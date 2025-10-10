"""
Validate and compare existing client with OpenAPI specification.

This script compares the manually written client code with the OpenAPI
specification to identify missing endpoints, deprecated methods, and
potential conflicts.
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class ClientValidator:
    """Validate client code against OpenAPI specification."""

    def __init__(self, spec: dict, client_path: Path):
        """
        Initialize the validator.

        Args:
            spec: OpenAPI specification dictionary
            client_path: Path to client.py file
        """
        self.spec = spec
        self.client_path = client_path
        self.spec_endpoints = self._extract_spec_endpoints()
        self.client_methods = self._extract_client_methods()

    def _extract_spec_endpoints(self) -> Dict[str, Dict]:
        """Extract all endpoints from OpenAPI spec."""
        endpoints = {}

        for path, path_item in self.spec.get("paths", {}).items():
            for method in ["get", "post", "put", "delete", "patch"]:
                if method in path_item:
                    operation = path_item[method]
                    operation_id = operation.get("operationId", f"{method}_{path}")
                    endpoints[operation_id] = {
                        "path": path,
                        "method": method,
                        "summary": operation.get("summary", ""),
                        "operation": operation,
                    }

        return endpoints

    def _extract_client_methods(self) -> Dict[str, Dict]:
        """Extract all methods from client Python file."""
        methods = {}

        if not self.client_path.exists():
            return methods

        with open(self.client_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private methods
                if not node.name.startswith("_"):
                    # Extract docstring
                    docstring = ast.get_docstring(node) or ""

                    # Extract parameters
                    params = [arg.arg for arg in node.args.args if arg.arg != "self"]

                    methods[node.name] = {
                        "docstring": docstring,
                        "params": params,
                        "lineno": node.lineno,
                    }

        return methods

    def find_missing_endpoints(self) -> List[Dict]:
        """Find endpoints in spec that are missing from client."""
        missing = []

        for operation_id, endpoint_info in self.spec_endpoints.items():
            # Check if any client method seems to match this endpoint
            path = endpoint_info["path"]
            method = endpoint_info["method"]

            # Generate expected method name patterns
            path_parts = [p for p in path.split("/") if p and not p.startswith("{")]
            expected_patterns = [
                f"{method}_{part}" for part in path_parts
            ] + path_parts

            # Check if any client method matches
            found = False
            for client_method in self.client_methods.keys():
                if any(pattern.lower() in client_method.lower() for pattern in expected_patterns):
                    found = True
                    break

            if not found:
                missing.append(
                    {
                        "operation_id": operation_id,
                        "path": path,
                        "method": method,
                        "summary": endpoint_info["summary"],
                    }
                )

        return missing

    def find_undocumented_methods(self) -> List[str]:
        """Find client methods that may not match any spec endpoint."""
        # This is a heuristic check
        undocumented = []

        for method_name, method_info in self.client_methods.items():
            # Check if method has a docstring
            if not method_info["docstring"]:
                undocumented.append(method_name)

        return undocumented

    def generate_report(self) -> str:
        """Generate validation report."""
        lines = []
        lines.append("=" * 70)
        lines.append("BMRS Client Validation Report")
        lines.append("=" * 70)
        lines.append("")

        # Summary
        lines.append("Summary:")
        lines.append(f"  - Spec endpoints: {len(self.spec_endpoints)}")
        lines.append(f"  - Client methods: {len(self.client_methods)}")
        lines.append("")

        # Missing endpoints
        missing = self.find_missing_endpoints()
        if missing:
            lines.append(f"Missing Endpoints ({len(missing)}):")
            lines.append("-" * 70)
            for endpoint in missing[:10]:  # Show first 10
                lines.append(f"  ✗ {endpoint['method'].upper():6} {endpoint['path']}")
                lines.append(f"    Summary: {endpoint['summary']}")
                lines.append(f"    Operation ID: {endpoint['operation_id']}")
                lines.append("")

            if len(missing) > 10:
                lines.append(f"  ... and {len(missing) - 10} more")
                lines.append("")
        else:
            lines.append("✓ No missing endpoints detected")
            lines.append("")

        # Undocumented methods
        undocumented = self.find_undocumented_methods()
        if undocumented:
            lines.append(f"Methods Without Docstrings ({len(undocumented)}):")
            lines.append("-" * 70)
            for method in undocumented:
                lines.append(f"  ⚠ {method}")
            lines.append("")
        else:
            lines.append("✓ All methods have docstrings")
            lines.append("")

        # Recommendations
        lines.append("Recommendations:")
        lines.append("-" * 70)
        if missing:
            lines.append("  1. Consider adding methods for missing endpoints")
            lines.append("  2. Run: python tools/generate_client.py")
            lines.append("  3. Review generated methods and integrate")
        else:
            lines.append("  ✓ Client appears to cover all documented endpoints")

        if undocumented:
            lines.append("  4. Add docstrings to undocumented methods")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)


def compare_schemas() -> Tuple[List[str], List[str]]:
    """
    Compare existing client with generated client.

    Returns:
        Tuple of (methods_only_in_existing, methods_only_in_generated)
    """
    script_dir = Path(__file__).parent
    existing_path = script_dir.parent / "elexon_bmrs" / "client.py"
    generated_path = script_dir.parent / "elexon_bmrs" / "generated_client.py"

    existing_methods = set()
    generated_methods = set()

    # Extract methods from existing client
    if existing_path.exists():
        with open(existing_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    existing_methods.add(node.name)

    # Extract methods from generated client
    if generated_path.exists():
        with open(generated_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    generated_methods.add(node.name)

    only_existing = sorted(existing_methods - generated_methods)
    only_generated = sorted(generated_methods - existing_methods)

    return only_existing, only_generated


def main() -> int:
    """Main entry point."""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 18 + "BMRS Client Validator" + " " * 19 + "║")
    print("╚" + "=" * 58 + "╝\n")

    script_dir = Path(__file__).parent
    spec_path = script_dir.parent / "schema" / "bmrs_openapi.json"
    client_path = script_dir.parent / "elexon_bmrs" / "client.py"

    # Check if spec exists
    if not spec_path.exists():
        print(f"✗ OpenAPI specification not found: {spec_path}")
        print("\nPlease run: python tools/download_schema.py first")
        return 1

    # Load spec
    print(f"Loading OpenAPI spec from: {spec_path}")
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    
    # Handle spec wrapped in array
    if isinstance(spec, list):
        if len(spec) > 0:
            spec = spec[0]
            print("Note: OpenAPI spec was wrapped in array, extracted first element")
        else:
            print("✗ Error: OpenAPI spec is an empty array")
            return 1

    # Validate
    print(f"Validating client: {client_path}\n")
    validator = ClientValidator(spec, client_path)
    report = validator.generate_report()
    print(report)

    # Compare with generated client if it exists
    print("\nComparing with generated client...")
    only_existing, only_generated = compare_schemas()

    if only_existing or only_generated:
        print("\nDifferences Found:")
        print("-" * 70)

        if only_existing:
            print(f"\nMethods only in existing client ({len(only_existing)}):")
            for method in only_existing[:10]:
                print(f"  • {method}")
            if len(only_existing) > 10:
                print(f"  ... and {len(only_existing) - 10} more")

        if only_generated:
            print(f"\nMethods only in generated client ({len(only_generated)}):")
            for method in only_generated[:10]:
                print(f"  + {method}")
            if len(only_generated) > 10:
                print(f"  ... and {len(only_generated) - 10} more")
    else:
        print("✓ No differences found between existing and generated clients")

    print("\n" + "=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

