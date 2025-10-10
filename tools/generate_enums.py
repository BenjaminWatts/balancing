"""
Generate enum types for BMRS API fields.

This script analyzes the OpenAPI spec to identify fields that should be enums
and generates Python Enum classes for them.
"""

import json
import re
from pathlib import Path
from typing import Dict, Set
from collections import defaultdict


class EnumGenerator:
    """Generate enum types from OpenAPI spec."""
    
    # Known enum fields from BMRS API documentation
    KNOWN_ENUMS = {
        'dataset': [
            'ABUC', 'AGPT', 'AGWS', 'AOBE', 'ATL', 'AWGF', 'B1610', 'B1620', 'B1630',
            'BEB', 'BOALF', 'BOD', 'CBS', 'CCM', 'CDN', 'DAG', 'DATL', 'DCI', 'DGWS',
            'DISBSAD', 'FEIB', 'FREQ', 'FUELINST', 'IGCA', 'IGCPU', 'INDDEM', 'INDGEN',
            'INDOD', 'LOLPDRM', 'MATL', 'MDP', 'MDV', 'MID', 'MILS', 'MNZT', 'MZT',
            'NDZ', 'NETBSAD', 'NONBM', 'NTB', 'NTO', 'PBC', 'PN', 'PPBR', 'QAS', 'QPN',
            'REMIT', 'RURE', 'RZDF', 'RZDR', 'SEL', 'SIL', 'SOSO', 'SYSWARN', 'TEMP',
            'TUDM', 'UOU', 'WATL', 'YAFM', 'YATL'
        ],
        'psrType': [
            'Generation', 'Solar', 'Wind Onshore', 'Wind Offshore', 'Hydro Pumped Storage',
            'Hydro Run-of-river and poundage', 'Other', 'Fossil Gas', 'Fossil Hard coal',
            'Fossil Oil', 'Nuclear', 'Biomass', 'Waste', 'Geothermal', 'Marine'
        ],
        'fuelType': [
            'BIOMASS', 'CCGT', 'COAL', 'GAS', 'HYDRO', 'NUCLEAR', 'NPSHYD', 'OCGT',
            'OIL', 'OTHER', 'PS', 'WIND', 'INTEW', 'INTFR', 'INTIRL', 'INTNED',
            'INTNEM', 'INTNSL', 'Fossil Gas', 'Fossil Hard coal', 'Fossil Oil',
            'Nuclear', 'Biomass', 'Waste', 'Geothermal', 'Solar', 'Wind Onshore',
            'Wind Offshore', 'Hydro Pumped Storage', 'Hydro Run-of-river and poundage',
            'Marine', 'Other'
        ],
        'businessType': [
            'Production', 'Internal trade', 'Consumption', 'Solar generation',
            'Wind generation', 'Installed generation', 'Replacement reserve',
            'Frequency restoration reserve', 'Automatic frequency restoration reserve',
            'Congestion costs', 'Positive forecast margin', 'Negative forecast margin'
        ],
        'messageType': [
            'FPN', 'MEL', 'MIL', 'BOA', 'BOALF', 'QPN', 'DISEBSP', 'NETEBSP',
            'UnavailabilitiesOfElectricityFacilities', 'UnavailabilitiesOfProductionUnits',
            'UnavailabilitiesOfTransmissionInfrastructure'
        ],
        'eventType': [
            'Production unavailability', 'Transmission unavailability',
            'Offshore unavailability', 'Consumption unavailability'
        ],
        'processType': [
            'Day ahead', 'Intraday process', 'Realised', 'Week ahead',
            'Month ahead', 'Year ahead'
        ],
        'warningType': [
            'Demand Control Imminent', 'Demand Control Active', 'Demand Control Complete',
            'Insufficient System Margin', 'SO-SO TRADES', 'IT SYSTEMS OUTAGE',
            'Negative Reserve Active', 'Negative Reserve Imminent'
        ],
        'assetType': [
            'Production', 'Consumption', 'Transmission', 'Offshore'
        ],
        'eventStatus': [
            'Active', 'Inactive', 'Withdrawn', 'Cancelled', 'Completed'
        ],
        'unavailabilityType': [
            'Planned', 'Unplanned', 'Forced'
        ],
        'flowDirection': [
            'Up', 'Down'
        ],
        'tradeDirection': [
            'A01', 'A02'  # A01 = Import, A02 = Export
        ],
        'marketAgreementType': [
            'Daily', 'Weekly', 'Monthly', 'Yearly', 'Total'
        ],
        'boundary': [
            'GB', 'GB-IRL', 'GB-NIR', 'GB-FRA', 'GB-NED', 'GB-BEL', 'GB-NOR', 'GB-DEN'
        ],
        'recordType': [
            'ITSDO', 'LOLP', 'MELNGC', 'NDZ', 'NTB', 'NTO', 'RDRE', 'RURE', 'TSDO'
        ],
        'deliveryMode': [
            'Offtaking', 'Delivering'
        ],
        'settlementRunType': [
            'II', 'SF', 'R1', 'R2', 'R3', 'RF', 'DF'
        ],
        'bmUnitType': [
            'T', 'E', 'I', 'G', 'S', 'M'
        ],
        'priceDerivationCode': [
            'N', 'P', 'R', 'D'
        ],
        'systemZone': [
            'GB', 'GB-IRL', 'GB-NIR'
        ],
        'amendmentFlag': [
            'ORI', 'REP'
        ],
    }
    
    def __init__(self, spec: dict):
        """Initialize with OpenAPI spec."""
        self.spec = spec
        self.schemas = spec.get("components", {}).get("schemas", {})
        self.field_examples = defaultdict(set)
        self._extract_examples()
    
    def _extract_examples(self):
        """Extract example values from the spec."""
        for schema_name, schema in self.schemas.items():
            properties = schema.get('properties', {})
            for field_name, field_def in properties.items():
                # Check for examples
                if 'example' in field_def:
                    ex = field_def['example']
                    if isinstance(ex, (str, int, float, bool)):
                        self.field_examples[field_name].add(str(ex))
                if 'examples' in field_def:
                    examples = field_def['examples']
                    if isinstance(examples, list):
                        for ex in examples:
                            if isinstance(ex, (str, int, float, bool)):
                                self.field_examples[field_name].add(str(ex))
    
    def sanitize_enum_name(self, value: str) -> str:
        """Convert a value to a valid Python enum member name."""
        # Replace spaces and special characters with underscores
        name = re.sub(r'[^a-zA-Z0-9_]', '_', value)
        # Remove consecutive underscores
        name = re.sub(r'_+', '_', name)
        # Remove leading/trailing underscores
        name = name.strip('_')
        # Ensure it starts with a letter or underscore
        if name and name[0].isdigit():
            name = f'_{name}'
        # Convert to uppercase for enum convention
        name = name.upper()
        return name or 'UNKNOWN'
    
    def generate_enum_class(self, enum_name: str, values: list) -> str:
        """Generate a Python Enum class."""
        lines = []
        lines.append(f"class {enum_name}(str, Enum):")
        lines.append(f'    """Enum for {enum_name} field values."""')
        lines.append("")
        
        # Track used names to handle duplicates
        used_names = set()
        
        for value in sorted(values):
            member_name = self.sanitize_enum_name(value)
            
            # Handle duplicate names
            if member_name in used_names:
                # Add numeric suffix
                counter = 2
                while f"{member_name}_{counter}" in used_names:
                    counter += 1
                member_name = f"{member_name}_{counter}"
            
            used_names.add(member_name)
            
            # Generate the enum member
            lines.append(f'    {member_name} = "{value}"')
        
        return "\n".join(lines)
    
    def generate_all_enums(self) -> str:
        """Generate all enum classes."""
        enums = []
        
        # Generate enums for known enum fields
        for field_name, values in sorted(self.KNOWN_ENUMS.items()):
            # Convert field name to class name (e.g., psrType -> PsrType)
            class_name = ''.join(word.capitalize() for word in re.split(r'[_\s]+', field_name))
            if not class_name.endswith('Enum'):
                class_name += 'Enum'
            
            enum_code = self.generate_enum_class(class_name, values)
            enums.append(enum_code)
        
        # Build header
        header = '''"""
Auto-generated Enum types for BMRS API fields.

This file contains enum definitions for fields that have a known set of values,
providing better type safety and IDE autocomplete.

This file is automatically generated. Do not edit manually.
"""

from enum import Enum


'''
        
        return header + "\n\n\n".join(enums) + "\n"


def main():
    """Main entry point."""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "BMRS Enum Generator" + " " * 24 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    # Load the OpenAPI spec
    script_dir = Path(__file__).parent
    spec_path = script_dir.parent / "schema" / "bmrs_openapi.json"
    
    if not spec_path.exists():
        print(f"✗ OpenAPI specification not found: {spec_path}")
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
    
    # Generate enums
    print("Generating enum types...")
    generator = EnumGenerator(spec)
    enums_code = generator.generate_all_enums()
    
    # Save generated enums
    output_path = script_dir.parent / "elexon_bmrs" / "enums.py"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(enums_code)
    
    print(f"✓ Generated enums saved to: {output_path}")
    
    # Print statistics
    enum_count = len(generator.KNOWN_ENUMS)
    total_values = sum(len(values) for values in generator.KNOWN_ENUMS.values())
    print(f"\n✓ Generated {enum_count} enum types with {total_values} total values")
    
    print("\nGenerated enums:")
    for field_name, values in sorted(generator.KNOWN_ENUMS.items()):
        class_name = ''.join(word.capitalize() for word in re.split(r'[_\s]+', field_name))
        if not class_name.endswith('Enum'):
            class_name += 'Enum'
        print(f"  - {class_name}: {len(values)} values")
    
    print("\nNext steps:")
    print("  1. Review generated enums: elexon_bmrs/enums.py")
    print("  2. Update generate_models.py to use these enums")
    print("  3. Regenerate models: python tools/generate_models.py")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

