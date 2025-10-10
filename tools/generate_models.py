"""
Generate Pydantic models from OpenAPI specification.

This script reads the BMRS OpenAPI specification and generates
Pydantic models for all schema definitions.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Optional


class PydanticModelGenerator:
    """Generate Pydantic models from OpenAPI schemas."""

    # OpenAPI type to Python type mapping
    TYPE_MAPPING = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "List",
        "object": "Dict[str, Any]",
    }

    # OpenAPI format to Python type mapping
    FORMAT_MAPPING = {
        "date": "date",
        "date-time": "datetime",
        "int32": "int",
        "int64": "int",
        "float": "float",
        "double": "float",
    }

    def __init__(self, spec: dict):
        """
        Initialize the generator.

        Args:
            spec: OpenAPI specification dictionary
        """
        self.spec = spec
        self.schemas = spec.get("components", {}).get("schemas", {})
        self.generated_models: Set[str] = set()
        self.class_name_counts: Dict[str, int] = {}  # Track name collisions
        self.imports: Set[str] = set()
        
        # Add base imports
        self.base_imports = [
            "from typing import Any, Dict, List, Optional, Union",
            "from datetime import date, datetime",
            "from pydantic import BaseModel, Field, ConfigDict",
        ]
        self.imports: Set[str] = set()
        self.uses_enums = False
        self.uses_validators = False
        self.uses_field_mixins = False
        
        # Map field combinations to field mixin classes
        self.field_mixin_map = {
            frozenset(['settlementDate', 'settlementPeriod']): 'SettlementFields',
            frozenset(['timeFrom', 'timeTo']): 'TimeRangeFields',
            frozenset(['levelFrom', 'levelTo']): 'LevelRangeFields',
            frozenset(['bmUnit', 'nationalGridBmUnit']): 'BmUnitFields',
            frozenset(['documentId', 'documentRevisionNumber']): 'DocumentFields',
        }
        
        # Map single fields to field mixin classes
        self.single_field_mixin_map = {
            'publishTime': 'PublishTimeFields',
            'startTime': 'StartTimeFields',
            'dataset': 'DatasetFields',
            'quantity': 'QuantityFields',
            'price': 'PriceFields',
            'volume': 'VolumeFields',
            'demand': 'DemandFields',
            'generation': 'GenerationFields',
            'year': 'YearFields',
            'week': 'WeekFields',
            'forecastDate': 'ForecastDateFields',
            'boundary': 'BoundaryFields',
            'createdDateTime': 'CreatedDateTimeFields',
        }
        
        # Map field names to their enum types
        self.field_to_enum = {
            'dataset': 'DatasetEnum',
            'psrType': 'PsrtypeEnum',
            'fuelType': 'FueltypeEnum',
            'businessType': 'BusinesstypeEnum',
            'messageType': 'MessagetypeEnum',
            'eventType': 'EventtypeEnum',
            'processType': 'ProcesstypeEnum',
            'warningType': 'WarningtypeEnum',
            'assetType': 'AssettypeEnum',
            'eventStatus': 'EventstatusEnum',
            'unavailabilityType': 'UnavailabilitytypeEnum',
            'flowDirection': 'FlowdirectionEnum',
            'tradeDirection': 'TradedirectionEnum',
            'marketAgreementType': 'MarketagreementtypeEnum',
            'boundary': 'BoundaryEnum',
            'recordType': 'RecordtypeEnum',
            'deliveryMode': 'DeliverymodeEnum',
            'settlementRunType': 'SettlementruntypeEnum',
            'bmUnitType': 'BmunittypeEnum',
            'priceDerivationCode': 'PricederivationcodeEnum',
            'systemZone': 'SystemzoneEnum',
            'amendmentFlag': 'AmendmentflagEnum',
        }
        
        # Fields that should be inferred as required (not optional)
        # Based on BMRS API usage patterns - these are fields that are
        # consistently present in API responses
        self.inferred_required_fields = {
            # Core identification fields - ALWAYS present
            'dataset', 'documentId', 'publishTime', 'settlementDate', 'settlementPeriod',
            'startTime', 'timeFrom', 'measurementTime', 'createdDateTime',
            'halfHourEndTime', 'messageReceivedDateTime', 'documentRevisionNumber',
            'timeSeriesId', 'mrid', 'mRID', 'createdTime',
            
            # Settlement period ranges
            'settlementPeriodFrom', 'settlementPeriodTo',
            
            # BM Unit identification - present when relevant
            'bmUnit', 'nationalGridBmUnit', 'nationalGridBmUnitId', 'bmUnitType',
            
            # Core data fields - the actual data values
            'quantity', 'generation', 'demand', 'price', 'cost', 'volume',
            'frequency', 'temperature', 'transmissionSystemDemand', 'nationalDemand',
            'outputUsable', 'margin', 'surplus', 'imbalance',
            
            # Status and type fields - classification data
            'businessType', 'psrType', 'fuelType', 'messageType', 'processType',
            'warningType', 'messageHeading', 'eventType', 'unavailabilityType',
            'assetType', 'eventStatus', 'amendmentFlag',
            
            # ID fields - identifiers
            'id', 'acceptanceNumber', 'pairId', 'acceptanceId',
            'participantId', 'assetId', 'affectedUnit', 'demandControlId',
            'bidId', 'sequenceId', 'messageId',
            
            # Direction and flow fields
            'flowDirection', 'tradeDirection',
            
            # Contract and market fields
            'marketAgreementType', 'contractIdentification',
            
            # Trade fields
            'tradeQuantity', 'tradePrice', 'traderUnit',
            
            # Capacity and limit fields that are typically present
            'normalCapacity', 'availableCapacity', 'unavailableCapacity',
            
            # Time-related fields
            'eventStartTime', 'eventEndTime', 'acceptanceTime',
            'publishingPeriodCommencingTime',
            
            # Location/zone fields
            'affectedArea', 'biddingZone', 'systemZone', 'interconnectorName',
            
            # Forecast fields
            'forecastDate', 'forecastWeek', 'forecastYear', 'weekStartDate',
            'calendarWeekNumber',
            
            # Other commonly required fields
            'cause', 'revisionNumber', 'affectedDso',
            'instructionSequence', 'demandControlEventFlag',
            'leadPartyName', 'leadPartyId', 'gspGroupId',
            'minimumPossible', 'maximumAvailable',
            'amount', 'energyPrice', 'procurementPrice',
        }

    def sanitize_class_name(self, name: str, original_name: str = None) -> str:
        """
        Convert schema name to valid Python class name.
        
        Handles duplicate class names from OpenAPI wrapper types by adding
        descriptive suffixes. For example:
        - "...DatasetRows.AbucDatasetRow" → "AbucDatasetRow"
        - "...DatasetResponse-1_...AbucDatasetRow" → "AbucDatasetRow_DatasetResponse"

        Args:
            name: Original schema name
            original_name: Full original name for context (used for uniqueness)

        Returns:
            Sanitized class name with suffix if needed
        """
        original_name = original_name or name
        
        # Detect wrapper types and add descriptive suffixes
        # This resolves duplicate class names from generic wrapper types
        suffix = ""
        if "DatasetResponse-1_" in original_name:
            suffix = "_DatasetResponse"
        elif "ResponseWithMetadata-1_" in original_name:
            suffix = "_ResponseWithMetadata"
        elif "Response-1_" in original_name and "-1_" in original_name:
            suffix = "_Response"
        
        # Remove namespace prefixes (e.g., "Insights.Api.Models.")
        name = name.split(".")[-1]
        
        # Replace invalid characters
        name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        
        # Remove consecutive underscores
        name = re.sub(r"_+", "_", name)
        
        # Ensure it starts with a letter
        if name and name[0].isdigit():
            name = f"Model_{name}"
        
        # Remove leading/trailing underscores
        name = name.strip("_")
        
        # Add suffix for wrapper types
        result = (name + suffix) if suffix else name
        
        return result or "UnnamedModel"

    def sanitize_field_name(self, name: str) -> str:
        """
        Convert field name to valid Python identifier in snake_case.

        Args:
            name: Original field name (e.g., 'publishTime', 'bmUnit')

        Returns:
            Sanitized field name in snake_case (e.g., 'publish_time', 'bm_unit')
        """
        # Convert camelCase to snake_case
        # Insert underscore before uppercase letters that follow lowercase letters
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
        # Convert to lowercase
        name = name.lower()
        
        # Replace invalid characters
        name = re.sub(r"[^a-z0-9_]", "_", name)
        
        # Python keywords need underscore suffix
        python_keywords = {
            'from', 'to', 'in', 'is', 'or', 'and', 'not', 'if', 'else',
            'for', 'while', 'def', 'class', 'return', 'import', 'as'
        }
        
        if name in python_keywords:
            name = f"{name}_"
        
        # Remove consecutive underscores
        name = re.sub(r"_+", "_", name)
        
        return name.strip("_") or "field"

    def get_python_type(self, schema: Dict[str, Any], required: bool = False, field_name: str = None) -> str:
        """
        Convert OpenAPI schema to Python type hint.

        Args:
            schema: OpenAPI schema definition
            required: Whether the field is required
            field_name: Name of the field (used for enum lookup)

        Returns:
            Python type hint string
        """
        # Check if this field should use an enum
        if field_name and field_name in self.field_to_enum:
            enum_type = self.field_to_enum[field_name]
            # Mark that we use enums
            self.uses_enums = True
            type_hint = enum_type
        # Handle $ref references
        elif "$ref" in schema:
            ref_path = schema["$ref"]
            ref_name = ref_path.split("/")[-1]
            class_name = self.sanitize_class_name(ref_name, original_name=ref_name)
            type_hint = class_name
        # Handle arrays
        elif schema.get("type") == "array":
            items = schema.get("items", {})
            item_type = self.get_python_type(items, required=True, field_name=field_name)
            type_hint = f"List[{item_type}]"
        # Handle nullable fields
        elif schema.get("nullable") or not required:
            base_type = self._get_base_type(schema, field_name=field_name)
            return f"Optional[{base_type}]"
        else:
            type_hint = self._get_base_type(schema, field_name=field_name)

        # Make optional if not required
        if not required and not type_hint.startswith("Optional"):
            type_hint = f"Optional[{type_hint}]"

        return type_hint

    def _get_base_type(self, schema: Dict[str, Any], field_name: str = None) -> str:
        """Get base Python type from schema."""
        schema_type = schema.get("type", "string")
        schema_format = schema.get("format")

        # Check format first
        if schema_format and schema_format in self.FORMAT_MAPPING:
            return self.FORMAT_MAPPING[schema_format]

        # Then check type
        return self.TYPE_MAPPING.get(schema_type, "Any")

    def _detect_mixins(self, properties: Dict[str, Any]) -> tuple[List[str], Set[str]]:
        """
        Detect which mixins should be applied based on the fields present.
        
        Args:
            properties: Model properties
            
        Returns:
            Tuple of (mixin class names, fields to skip because they're in mixins)
        """
        mixins = []
        fields_to_skip = set()
        field_names = set(properties.keys())
        
        # Order matters: more specific mixins first, then general ones
        
        # Check for field combinations that have field mixins
        for field_combo, mixin_name in self.field_mixin_map.items():
            if field_combo.issubset(field_names):
                mixins.append(mixin_name)
                fields_to_skip.update(field_combo)
                self.uses_field_mixins = True
        
        # Check for single fields that have field mixins
        for field_name, mixin_name in self.single_field_mixin_map.items():
            if field_name in field_names and field_name not in fields_to_skip:
                mixins.append(mixin_name)
                fields_to_skip.add(field_name)
                self.uses_field_mixins = True
        
        # Now add validator mixins (methods only, no fields)
        # These are for fields NOT covered by field mixins
        
        # Settlement date without period
        if 'settlementDate' in field_names and 'settlementDate' not in fields_to_skip:
            mixins.append('SettlementDateMixin')
            self.uses_validators = True
        
        # Single field mixins (alphabetically)
        
        # Acceptance (3+ models)
        if 'acceptanceNumber' in field_names:
            mixins.append('AcceptanceMixin')
            self.uses_validators = True
        
        # Affected unit (4 models)
        if 'affectedUnit' in field_names:
            mixins.append('AffectedUnitMixin')
            self.uses_validators = True
        
        # Asset (6+ models)
        if 'assetId' in field_names:
            mixins.append('AssetMixin')
            self.uses_validators = True
        
        # Bid/Offer (multiple models)
        if 'bid' in field_names and 'offer' in field_names:
            mixins.append('BidOfferMixin')
            self.uses_validators = True
        
        # BM Unit fields (22+ models)
        if 'bmUnit' in field_names or 'nationalGridBmUnit' in field_names:
            mixins.append('BmUnitMixin')
            self.uses_validators = True
        
        # Business type (10 models)
        if 'businessType' in field_names:
            mixins.append('BusinessTypeMixin')
            self.uses_validators = True
        
        # Capacity (multiple models)
        if 'normalCapacity' in field_names or 'availableCapacity' in field_names:
            mixins.append('CapacityMixin')
            self.uses_validators = True
        
        # Created date time (6 models)
        if 'createdDateTime' in field_names:
            mixins.append('CreatedDateTimeMixin')
            self.uses_validators = True
        
        # Dataset (many models)
        if 'dataset' in field_names:
            mixins.append('DatasetMixin')
            self.uses_validators = True
        
        # Event (4 models)
        if 'eventType' in field_names and 'eventStatus' in field_names:
            mixins.append('EventMixin')
            self.uses_validators = True
        
        # Event time (multiple models)
        if 'eventStartTime' in field_names and 'eventEndTime' in field_names:
            mixins.append('EventTimeMixin')
            self.uses_validators = True
        
        # Flags (multiple models)
        if any(f in field_names for f in ['deemedBoFlag', 'soFlag', 'storFlag', 'rrFlag']):
            mixins.append('FlagsMixin')
            self.uses_validators = True
        
        # Flow direction (6+ models) - includes validation
        if 'flowDirection' in field_names:
            mixins.append('FlowDirectionMixin')
            self.uses_validators = True
        
        # Fuel type (12 models)
        if 'fuelType' in field_names:
            mixins.append('FuelTypeMixin')
            self.uses_validators = True
        
        # Lead party (multiple models)
        if 'leadPartyName' in field_names:
            mixins.append('LeadPartyMixin')
            self.uses_validators = True
        
        # Message (4 models)
        if 'messageHeading' in field_names and 'messageType' in field_names:
            mixins.append('MessageMixin')
            self.uses_validators = True
        
        # MRID (3+ models)
        if 'mrid' in field_names or 'mRID' in field_names:
            mixins.append('MridMixin')
            self.uses_validators = True
        
        # Pair ID (multiple models)
        if 'pairId' in field_names:
            mixins.append('PairIdMixin')
            self.uses_validators = True
        
        # Participant (3+ models)
        if 'participantId' in field_names:
            mixins.append('ParticipantMixin')
            self.uses_validators = True
        
        # Volume (8 models)
        if 'volume' in field_names:
            mixins.append('VolumeMixin')
            self.uses_validators = True
        
        # Cost (3+ models)
        if 'cost' in field_names:
            mixins.append('CostMixin')
            self.uses_validators = True
        
        # Demand (3+ models)
        if 'demand' in field_names:
            mixins.append('DemandMixin')
            self.uses_validators = True
        
        # Generation (3+ models)
        if 'generation' in field_names:
            mixins.append('GenerationMixin')
            self.uses_validators = True
        
        # Margin (5 models)
        if 'margin' in field_names:
            mixins.append('MarginMixin')
            self.uses_validators = True
        
        # Surplus (4 models)
        if 'surplus' in field_names:
            mixins.append('SurplusMixin')
            self.uses_validators = True
        
        # Imbalance (multiple models)
        if 'imbalance' in field_names:
            mixins.append('ImbalanceMixin')
            self.uses_validators = True
        
        # Frequency (multiple models)
        if 'frequency' in field_names:
            mixins.append('FrequencyMixin')
            self.uses_validators = True
        
        # Temperature (multiple models)
        if 'temperature' in field_names:
            mixins.append('TemperatureMixin')
            self.uses_validators = True
        
        # Year (14 models)
        if 'year' in field_names:
            mixins.append('YearMixin')
            self.uses_validators = True
        
        # Week (7 models)
        if 'week' in field_names:
            mixins.append('WeekMixin')
            self.uses_validators = True
        
        # Month (multiple models)
        if 'month' in field_names:
            mixins.append('MonthMixin')
            self.uses_validators = True
        
        # Forecast date (13 models)
        if 'forecastDate' in field_names:
            mixins.append('ForecastDateMixin')
            self.uses_validators = True
        
        # Boundary (10 models)
        if 'boundary' in field_names:
            mixins.append('BoundaryMixin')
            self.uses_validators = True
        
        # Output usable (8 models)
        if 'outputUsable' in field_names:
            mixins.append('OutputUsableMixin')
            self.uses_validators = True
        
        # Bidding zone (5 models)
        if 'biddingZone' in field_names:
            mixins.append('BiddingZoneMixin')
            self.uses_validators = True
        
        # Interconnector (4 models)
        if 'interconnectorName' in field_names:
            mixins.append('InterconnectorMixin')
            self.uses_validators = True
        
        # Price (50+ models)
        if 'price' in field_names:
            mixins.append('PriceMixin')
            self.uses_validators = True
        
        # PSR type (13 models)
        if 'psrType' in field_names:
            mixins.append('PsrTypeMixin')
            self.uses_validators = True
        
        # Publish time (86 models)
        if 'publishTime' in field_names:
            mixins.append('PublishTimeMixin')
            self.uses_validators = True
        
        # Quantity (80+ models)
        if 'quantity' in field_names:
            mixins.append('QuantityMixin')
            self.uses_validators = True
        
        # Revision number (7 models)
        if 'revisionNumber' in field_names:
            mixins.append('RevisionMixin')
            self.uses_validators = True
        
        # Start time (56 models) - only if not already in field mixin
        if 'startTime' in field_names and 'startTime' not in fields_to_skip:
            mixins.append('StartTimeMixin')
            self.uses_validators = True
        
        return mixins, fields_to_skip

    def generate_model(self, name: str, schema: Dict[str, Any]) -> str:
        """
        Generate a Pydantic model from a schema.

        Args:
            name: Schema name
            schema: Schema definition

        Returns:
            Generated Python class code
        """
        class_name = self.sanitize_class_name(name, original_name=name)
        
        # Handle any remaining name collisions with numeric suffix
        # This is a fallback for edge cases not caught by suffix detection
        original_class_name = class_name
        if class_name in self.generated_models:
            # Add numeric suffix for collision
            if class_name not in self.class_name_counts:
                self.class_name_counts[class_name] = 1
            else:
                self.class_name_counts[class_name] += 1
            class_name = f"{class_name}_{self.class_name_counts[class_name]}"
        
        self.generated_models.add(class_name)

        # Get properties and required fields
        properties = schema.get("properties", {})
        required_fields = set(schema.get("required", []))
        description = schema.get("description", "")

        if not properties:
            # Empty model or allOf/oneOf/anyOf
            if "allOf" in schema or "oneOf" in schema or "anyOf" in schema:
                # Skip complex composition schemas for now
                return ""
            # Create a simple model
            properties = {}

        # Detect which mixins to apply and which fields to skip
        mixins, fields_to_skip = self._detect_mixins(properties)
        
        lines = []
        # Build class definition with mixins
        if mixins:
            base_classes = ', '.join(mixins + ['BaseModel'])
            lines.append(f"class {class_name}({base_classes}):")
        else:
            lines.append(f"class {class_name}(BaseModel):")
        
        # Add docstring
        if description:
            lines.append(f'    """{description}"""')
            lines.append("")

        # Add config - allow both snake_case and camelCase field names
        lines.append("    model_config = ConfigDict(extra='allow', populate_by_name=True)")
        lines.append("")

        # Generate fields (skip fields provided by field mixins)
        if properties:
            for field_name, field_schema in properties.items():
                # Skip fields that are provided by field mixins
                if field_name in fields_to_skip:
                    continue
                    
                safe_field_name = self.sanitize_field_name(field_name)
                # Check both OpenAPI required fields AND our inferred required fields
                # Override nullable if field is in our inferred required list
                is_required = field_name in required_fields or field_name in self.inferred_required_fields
                
                # Override the schema's nullable setting if we've inferred it's required
                if field_name in self.inferred_required_fields:
                    # Create a copy to avoid modifying the original
                    field_schema = field_schema.copy()
                    field_schema['nullable'] = False
                
                type_hint = self.get_python_type(field_schema, required=is_required, field_name=field_name)
                field_description = field_schema.get("description", "")
                example = field_schema.get("example")

                # Build field definition
                field_params = []
                
                # Always add alias if field name changed (for snake_case conversion)
                if safe_field_name != field_name:
                    field_params.append(f'alias="{field_name}"')
                
                if field_description:
                    field_params.append(f'description="{field_description}"')
                if example is not None:
                    if isinstance(example, str):
                        field_params.append(f'examples=["{example}"]')
                    else:
                        field_params.append(f'examples=[{example}]')
                
                # Generate field line
                if field_params:
                    if not is_required:
                        lines.append(f"    {safe_field_name}: {type_hint} = Field(default=None, {', '.join(field_params)})")
                    else:
                        lines.append(f"    {safe_field_name}: {type_hint} = Field({', '.join(field_params)})")
                else:
                    if not is_required:
                        lines.append(f"    {safe_field_name}: {type_hint} = None")
                    else:
                        lines.append(f"    {safe_field_name}: {type_hint}")

        else:
            # No properties, add pass
            lines.append("    pass")

        return "\n".join(lines)

    def generate_all_models(self) -> str:
        """
        Generate all Pydantic models from the spec.

        Returns:
            Complete Python code for all models
        """
        models = []

        # Sort schemas for consistent output
        sorted_schemas = sorted(self.schemas.items())

        for name, schema in sorted_schemas:
            model_code = self.generate_model(name, schema)
            if model_code:
                models.append(model_code)

        # Build header with succinct imports
        header = '''"""
Auto-generated Pydantic models from BMRS OpenAPI specification.

This file is automatically generated. Do not edit manually.
"""

from __future__ import annotations  # Enable forward references

from typing import Any, Dict, List, Optional, Union
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict
'''
        
        # Add enum and validator imports if used (succinct module imports)
        if self.uses_enums:
            header += "from elexon_bmrs import enums\n"
        if self.uses_validators:
            header += "from elexon_bmrs import validators\n"
        if self.uses_field_mixins:
            header += "from elexon_bmrs import field_mixins\n"
        
        header += "\n"
        
        # Add convenience aliases for field mixins
        if self.uses_field_mixins:
            header += "\n# Field mixin aliases (provide field definitions + methods)\n"
            all_field_mixins = set(self.field_mixin_map.values()) | set(self.single_field_mixin_map.values())
            for mixin in sorted(all_field_mixins):
                header += f"{mixin} = field_mixins.{mixin}\n"
        
        # Add convenience aliases for commonly used types
        if self.uses_enums:
            header += "\n# Enum type aliases for convenience\n"
            for field_name, enum_type in sorted(self.field_to_enum.items()):
                header += f"{enum_type} = enums.{enum_type}\n"
        
        if self.uses_validators:
            header += "\n# Validator mixin aliases for convenience\n"
            validator_mixins = [
                'SettlementPeriodMixin', 'SettlementDateMixin', 'TimeRangeMixin', 'LevelRangeMixin',
                'PublishTimeMixin', 'StartTimeMixin', 'DocumentMixin', 'DatasetMixin',
                'FlowDirectionMixin', 'BmUnitMixin', 'QuantityMixin', 'PriceMixin',
                'FuelTypeMixin', 'PsrTypeMixin', 'BusinessTypeMixin', 'CreatedDateTimeMixin',
                'RevisionMixin', 'AssetMixin', 'MessageMixin', 'EventMixin', 'EventTimeMixin',
                'AffectedUnitMixin', 'ParticipantMixin', 'AcceptanceMixin', 'BidOfferMixin',
                'PairIdMixin', 'FlagsMixin', 'CapacityMixin', 'LeadPartyMixin', 'MridMixin',
                'VolumeMixin', 'CostMixin', 'DemandMixin', 'GenerationMixin', 'MarginMixin',
                'SurplusMixin', 'ImbalanceMixin', 'FrequencyMixin', 'TemperatureMixin',
                'YearMixin', 'WeekMixin', 'MonthMixin', 'ForecastDateMixin', 'BoundaryMixin',
                'OutputUsableMixin', 'BiddingZoneMixin', 'InterconnectorMixin'
            ]
            for mixin in validator_mixins:
                header += f"{mixin} = validators.{mixin}\n"
        
        header += "\n\n"

        return header + "\n\n\n".join(models) + "\n"


def main() -> int:
    """Main entry point."""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "BMRS Model Generator" + " " * 23 + "║")
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

    # Handle spec wrapped in array
    if isinstance(spec, list):
        if len(spec) > 0:
            spec = spec[0]
            print("Note: OpenAPI spec was wrapped in array, extracted first element")
        else:
            print("✗ Error: OpenAPI spec is an empty array")
            return 1

    # Generate models
    print("Generating Pydantic models...")
    generator = PydanticModelGenerator(spec)
    models_code = generator.generate_all_models()

    # Save generated models
    output_path = script_dir.parent / "elexon_bmrs" / "generated_models.py"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(models_code)

    print(f"✓ Generated models saved to: {output_path}")

    # Print statistics
    model_count = len(generator.generated_models)
    schema_count = len(generator.schemas)
    print(f"\n✓ Generated {model_count} models from {schema_count} schemas")

    print("\nNext steps:")
    print("  1. Review generated models: {output_path}")
    print("  2. Update client methods to return typed responses")
    print("  3. Run tests to verify model compatibility")

    return 0


if __name__ == "__main__":
    sys.exit(main())

