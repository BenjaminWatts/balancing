"""
Generate client code from OpenAPI specification.

This script reads the BMRS OpenAPI specification and generates
Python client methods for all API endpoints.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class ClientCodeGenerator:
    """Generate Python client code from OpenAPI specification."""
    
    # Python reserved keywords that need to be escaped
    RESERVED_KEYWORDS = {
        'from', 'to', 'in', 'is', 'or', 'and', 'not', 'if', 'else', 'elif',
        'for', 'while', 'break', 'continue', 'def', 'class', 'return', 'yield',
        'import', 'as', 'pass', 'raise', 'try', 'except', 'finally', 'with',
        'lambda', 'global', 'nonlocal', 'assert', 'del', 'exec', 'print'
    }

    def __init__(self, spec: dict):
        """
        Initialize the generator.

        Args:
            spec: OpenAPI specification dictionary
        """
        self.spec = spec
        self.paths = spec.get("paths", {})
        self.components = spec.get("components", {})
        self.schemas = self.components.get("schemas", {})
        self.endpoint_to_model: Dict[str, str] = {}  # Map method names to response models

    def generate_method_name(self, path: str, method: str, operation_id: str = None) -> str:
        """
        Generate a Python method name from an API path.

        Args:
            path: API endpoint path
            method: HTTP method
            operation_id: OpenAPI operation ID if available

        Returns:
            Python method name
        """
        if operation_id:
            # Use operation ID if provided
            name = re.sub(r"[^a-zA-Z0-9_]", "_", operation_id)
            name = self._to_snake_case(name)
            # Remove consecutive underscores
            name = re.sub(r"_+", "_", name)
            name = name.strip("_")
            return name

        # Extract meaningful parts from path
        parts = [p for p in path.split("/") if p and not p.startswith("{")]

        # Remove common prefixes
        parts = [p for p in parts if p.lower() not in ["api", "v1", "v2", "bmrs"]]

        # Replace hyphens and invalid chars with underscores
        parts = [re.sub(r"[^a-zA-Z0-9_]", "_", p) for p in parts]

        # Create method name
        if method.lower() == "get":
            prefix = "get"
        elif method.lower() == "post":
            prefix = "create"
        elif method.lower() == "put":
            prefix = "update"
        elif method.lower() == "delete":
            prefix = "delete"
        else:
            prefix = method.lower()

        name = "_".join([prefix] + parts)
        name = self._to_snake_case(name)
        # Remove consecutive underscores
        name = re.sub(r"_+", "_", name)
        name = name.strip("_")
        return name

    def _to_snake_case(self, text: str) -> str:
        """Convert text to snake_case."""
        # Insert underscore before capitals
        text = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
        text = re.sub("([a-z0-9])([A-Z])", r"\1_\2", text)
        return text.lower()
    
    def _escape_param_name(self, name: str) -> str:
        """
        Escape parameter name if it's a Python reserved keyword.
        
        Args:
            name: Parameter name
            
        Returns:
            Escaped parameter name (adds underscore suffix if reserved)
        """
        if name.lower() in self.RESERVED_KEYWORDS:
            return f"{name}_"
        return name

    def extract_parameters(self, operation: dict) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract parameters from an operation.

        Args:
            operation: OpenAPI operation object

        Returns:
            Dictionary of parameters by location (query, path, header)
        """
        params = {"path": [], "query": [], "header": []}

        for param in operation.get("parameters", []):
            location = param.get("in", "query")
            if location in params:
                params[location].append(
                    {
                        "name": param.get("name"),
                        "required": param.get("required", False),
                        "type": self._get_param_type(param),
                        "description": param.get("description", ""),
                    }
                )

        return params

    def _get_param_type(self, param: dict) -> str:
        """Get Python type hint for parameter."""
        schema = param.get("schema", {})
        param_type = schema.get("type", "string")

        type_map = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "List[str]",
            "object": "Dict[str, Any]",
        }

        return type_map.get(param_type, "str")
    
    def _sanitize_class_name(self, name: str) -> str:
        """Convert schema name to valid Python class name (matches generate_models.py logic)."""
        # Handle wrapper type suffixes
        suffix = ""
        if "DatasetResponse-1_" in name:
            suffix = "_DatasetResponse"
        elif "ResponseWithMetadata-1_" in name:
            suffix = "_ResponseWithMetadata"
        elif "Response-1_" in name and "-1_" in name:
            suffix = "_Response"
        
        # Remove namespace prefixes
        name = name.split(".")[-1]
        
        # Replace invalid characters
        name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        name = re.sub(r"_+", "_", name)
        
        # Ensure it starts with a letter
        if name and name[0].isdigit():
            name = f"Model_{name}"
        
        name = name.strip("_")
        result = (name + suffix) if suffix else name
        
        return result or "UnnamedModel"
    
    def _get_response_model(self, operation: dict) -> str:
        """
        Extract the response model name from an operation.
        
        Returns the Pydantic model class name or 'Dict[str, Any]' if no specific model.
        """
        try:
            responses = operation.get('responses', {})
            success_response = responses.get('200', {})
            content = success_response.get('content', {})
            json_content = content.get('application/json', {})
            response_schema = json_content.get('schema', {})
            
            # Check if there's a $ref at the top level
            if '$ref' in response_schema:
                ref_path = response_schema['$ref']
                ref_name = ref_path.split("/")[-1]
                model_name = self._sanitize_class_name(ref_name)
                return model_name
            
            # Check if it's a direct array (e.g., /demand/outturn/summary returns array directly)
            if response_schema.get('type') == 'array':
                items = response_schema.get('items', {})
                if '$ref' in items:
                    ref_name = items['$ref'].split("/")[-1]
                    model_name = self._sanitize_class_name(ref_name)
                    # Return as List[Model]
                    return f"List[{model_name}]"
            
            # Check if it's an inline schema with properties and data array
            # This handles endpoints with wrapper objects
            if response_schema.get('type') == 'object':
                properties = response_schema.get('properties', {})
                
                # Common pattern: { data: [...], metadata: {...} }
                if 'data' in properties:
                    data_schema = properties['data']
                    
                    # If data is an array with items that have a $ref
                    if data_schema.get('type') == 'array':
                        items = data_schema.get('items', {})
                        if '$ref' in items:
                            ref_name = items['$ref'].split("/")[-1]
                            model_name = self._sanitize_class_name(ref_name)
                            # Return the wrapper model name (e.g., ModelName_DatasetResponse)
                            return f"{model_name}_DatasetResponse"
            
            # If no ref, return Dict (includes stream endpoints)
            return "Dict[str, Any]"
            
        except Exception:
            return "Dict[str, Any]"

    def generate_method(
        self, path: str, method: str, operation: dict
    ) -> str:
        """
        Generate Python method code for an API endpoint.

        Args:
            path: API endpoint path
            method: HTTP method
            operation: OpenAPI operation object

        Returns:
            Generated Python method code
        """
        method_name = self.generate_method_name(
            path, method, operation.get("operationId")
        )
        params = self.extract_parameters(operation)
        summary = operation.get("summary", "")
        description = operation.get("description", "")
        
        # Get the response model for this endpoint
        response_model = self._get_response_model(operation)
        self.endpoint_to_model[method_name] = response_model

        # Build method signature
        signature_params = ["self"]

        # Add path parameters
        for param in params["path"]:
            type_hint = param["type"]
            safe_name = self._escape_param_name(param['name'])
            signature_params.append(f"{safe_name}: {type_hint}")

        # Add required query parameters
        for param in params["query"]:
            if param["required"]:
                type_hint = param["type"]
                safe_name = self._escape_param_name(param['name'])
                signature_params.append(f"{safe_name}: {type_hint}")

        # Add optional query parameters
        for param in params["query"]:
            if not param["required"]:
                type_hint = param["type"]
                safe_name = self._escape_param_name(param['name'])
                signature_params.append(f"{safe_name}: Optional[{type_hint}] = None")

        signature = f"def {method_name}(\n        " + ",\n        ".join(signature_params) + f"\n    ) -> {response_model}:"

        # Build docstring
        docstring_lines = [f'        """']
        if summary:
            docstring_lines.append(f"        {summary}")
            docstring_lines.append("")

        if description and description != summary:
            docstring_lines.append(f"        {description}")
            docstring_lines.append("")

        if params["path"] or params["query"]:
            docstring_lines.append("        Args:")
            for param in params["path"] + params["query"]:
                required_str = "" if param["required"] else ", optional"
                safe_name = self._escape_param_name(param['name'])
                docstring_lines.append(
                    f"            {safe_name}: {param['description']}{required_str}"
                )
            docstring_lines.append("")

        docstring_lines.append("        Returns:")
        docstring_lines.append("            API response data")
        docstring_lines.append('        """')

        docstring = "\n".join(docstring_lines)

        # Build method body
        body_lines = []

        # Build params dict
        if params["query"]:
            body_lines.append("        params = {}")
            for param in params["query"]:
                param_name = param["name"]
                safe_name = self._escape_param_name(param_name)
                if param["required"]:
                    body_lines.append(f'        params["{param_name}"] = {safe_name}')
                else:
                    body_lines.append(f"        if {safe_name} is not None:")
                    body_lines.append(f'            params["{param_name}"] = {safe_name}')
        else:
            body_lines.append("        params = {}")

        # Build path with substitutions
        api_path = path
        for param in params["path"]:
            safe_name = self._escape_param_name(param['name'])
            api_path = api_path.replace(
                f"{{{param['name']}}}", f"{{{safe_name}}}"
            )

        body_lines.append("")
        body_lines.append(
            f'        response = self._make_request("{method.upper()}", f"{api_path}", params=params)'
        )
        
        # Add response parsing if we have a specific model
        if response_model != "Dict[str, Any]":
            body_lines.append(f"        ")
            body_lines.append(f"        # Parse response into Pydantic model(s)")
            
            # Check if it's a List[Model] return type
            if response_model.startswith("List["):
                # Extract the model name from List[ModelName]
                inner_model = response_model[5:-1]  # Remove "List[" and "]"
                body_lines.append(f"        if isinstance(response, list):")
                body_lines.append(f"            try:")
                body_lines.append(f"                return [{inner_model}(**item) for item in response]")
                body_lines.append(f"            except Exception as e:")
                body_lines.append(f"                import logging")
                body_lines.append(f'                logging.warning(f"Failed to parse list response as {response_model}: {{e}}. Returning raw data.")')
                body_lines.append(f"                return response")
                body_lines.append(f"        return response")
            else:
                # Single model or wrapped response
                body_lines.append(f"        if isinstance(response, dict):")
                body_lines.append(f"            try:")
                body_lines.append(f"                return {response_model}(**response)")
                body_lines.append(f"            except Exception as e:")
                body_lines.append(f"                import logging")
                body_lines.append(f'                logging.warning(f"Failed to parse response as {response_model}: {{e}}. Returning raw data.")')
                body_lines.append(f"                return response")
                body_lines.append(f"        return response")
        else:
            body_lines.append(f"        return response")

        body = "\n".join(body_lines)

        return f"    {signature}\n{docstring}\n{body}\n"

    def generate_all_methods(self) -> str:
        """
        Generate all client methods from the OpenAPI spec.

        Returns:
            Generated Python code for all methods
        """
        methods = []
        seen_method_names: Set[str] = set()

        for path, path_item in self.paths.items():
            for method in ["get", "post", "put", "delete", "patch"]:
                if method in path_item:
                    operation = path_item[method]
                    method_code = self.generate_method(path, method, operation)

                    # Extract method name to avoid duplicates
                    method_name = method_code.split("(")[0].strip().split()[-1]

                    if method_name not in seen_method_names:
                        methods.append(method_code)
                        seen_method_names.add(method_name)

        return "\n".join(methods)

    def generate_full_client(self) -> str:
        """
        Generate complete client file.

        Returns:
            Complete Python client code
        """
        header = '''"""
Auto-generated BMRS API client methods with typed Pydantic model returns.

This file is automatically generated from the OpenAPI specification.
Do not edit manually - changes will be overwritten.

All methods return properly typed Pydantic models for type safety and IDE autocomplete.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import date, datetime

# Import all generated models
from elexon_bmrs.generated_models import *


class GeneratedBMRSMethods:
    """
    Auto-generated methods for the BMRS API with typed returns.
    
    All methods return Pydantic models instead of Dict[str, Any] for:
    - Type safety
    - IDE autocomplete
    - Validation
    - Better developer experience
    """

'''

        methods = self.generate_all_methods()

        return header + methods


def main() -> int:
    """Main entry point."""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "BMRS Client Code Generator" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝\n")

    # Load the OpenAPI spec
    script_dir = Path(__file__).parent
    spec_path = script_dir.parent / "schema" / "bmrs_openapi.json"

    if not spec_path.exists():
        print(f"✗ OpenAPI specification not found: {spec_path}")
        print("\nPlease run: python tools/download_schema.py first")
        return 1

    print(f"Loading OpenAPI spec from: {spec_path}")
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    
    # Handle spec wrapped in array (some APIs return [spec] instead of spec)
    if isinstance(spec, list):
        if len(spec) > 0:
            spec = spec[0]
            print("Note: OpenAPI spec was wrapped in array, extracted first element")
        else:
            print("✗ Error: OpenAPI spec is an empty array")
            return 1

    # Generate client code
    print("Generating client methods...")
    generator = ClientCodeGenerator(spec)
    client_code = generator.generate_full_client()

    # Save generated code
    output_path = script_dir.parent / "elexon_bmrs" / "generated_client.py"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(client_code)

    print(f"✓ Generated client code saved to: {output_path}")

    # Print statistics
    method_count = client_code.count("def ")
    print(f"\n✓ Generated {method_count} methods")

    print("\nNext steps:")
    print("  1. Review generated code: {output_path}")
    print("  2. Run: python tools/validate_client.py")
    print("  3. Integrate with main client: elexon_bmrs/client.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())

