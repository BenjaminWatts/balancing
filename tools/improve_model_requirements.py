"""
Improve model requirements by analyzing field usage patterns.

This script analyzes the generated models and makes educated guesses about
which fields should be required based on common patterns and field names.
"""

import re
from pathlib import Path
from typing import Set, Dict, List


class ModelRequirementAnalyzer:
    """Analyze and improve model field requirements."""
    
    # Fields that are commonly required based on BMRS API patterns
    COMMONLY_REQUIRED_FIELDS = {
        # Core identification fields
        'dataset', 'documentId', 'publishTime', 'settlementDate', 'settlementPeriod',
        
        # Time fields (usually required for temporal data)
        'startTime', 'endTime', 'timeFrom', 'timeTo', 'measurementTime',
        'createdDateTime', 'messageReceivedDateTime',
        
        # BM Unit identification
        'bmUnit', 'nationalGridBmUnit', 'nationalGridBmUnitId',
        
        # Core data fields
        'quantity', 'generation', 'demand', 'price', 'cost', 'volume',
        
        # Status and type fields
        'businessType', 'psrType', 'fuelType', 'status', 'messageType',
        
        # ID fields
        'id', 'mrid', 'acceptanceNumber', 'pairId', 'timeSeriesId',
    }
    
    # Fields that are commonly optional (nullable/empty values expected)
    COMMONLY_OPTIONAL_FIELDS = {
        # Description and metadata
        'description', 'relatedInformation', 'messageText', 'warningText',
        
        # Flags and indicators
        'flag', 'indicator', 'specified', 'amendmentFlag', 'deemedBoFlag',
        'soFlag', 'storFlag', 'rrFlag', 'activeFlag', 'isTendered',
        
        # Optional numeric fields
        'percentage', 'ratio', 'multiplier', 'adjustment', 'deratedMargin',
        
        # Optional capacity/limit fields
        'capacity', 'limit', 'minimum', 'maximum', 'available', 'unavailable',
        
        # Optional time fields that might not always be present
        'endTime', 'timeTo', 'eventEndTime', 'clearedDefaultSettlementDate',
        
        # Optional location/area fields
        'area', 'zone', 'boundary', 'region', 'gspGroupId', 'gspGroupName',
    }
    
    # Field name patterns that suggest optional fields
    OPTIONAL_PATTERNS = [
        r'.*Flag$',           # *_flag fields
        r'.*Percentage$',     # *_percentage fields  
        r'.*Ratio$',          # *_ratio fields
        r'.*Adjustment$',     # *_adjustment fields
        r'.*Optional$',       # *_optional fields
        r'.*Available$',      # *_available fields
        r'.*Unavailable$',    # *_unavailable fields
        r'.*Specified$',      # *_specified fields
        r'.*Minimum$',        # *_minimum fields
        r'.*Maximum$',        # *_maximum fields
        r'.*Average$',        # *_average fields
        r'.*Total$',          # *_total fields
        r'.*Net$',            # *_net fields
        r'.*Secondary.*',     # secondary_* fields
        r'.*Reference.*',     # reference_* fields
        r'.*Effective.*',     # effective_* fields
        r'.*Amendment.*',     # amendment_* fields
    ]
    
    def __init__(self):
        """Initialize the analyzer."""
        self.required_fields: Dict[str, Set[str]] = {}
        self.optional_fields: Dict[str, Set[str]] = {}
    
    def analyze_field_name(self, field_name: str) -> bool:
        """
        Analyze a field name to determine if it should be required.
        
        Args:
            field_name: The field name to analyze
            
        Returns:
            True if the field should be required, False if optional
        """
        # Check against commonly required fields
        if field_name in self.COMMONLY_REQUIRED_FIELDS:
            return True
            
        # Check against commonly optional fields
        if field_name in self.COMMONLY_OPTIONAL_FIELDS:
            return False
            
        # Check against optional patterns
        for pattern in self.OPTIONAL_PATTERNS:
            if re.match(pattern, field_name, re.IGNORECASE):
                return False
                
        # Default to required for unknown fields (conservative approach)
        return True
    
    def analyze_model(self, class_name: str, fields: List[str]) -> Dict[str, bool]:
        """
        Analyze a model's fields to determine requirements.
        
        Args:
            class_name: Name of the model class
            fields: List of field names in the model
            
        Returns:
            Dictionary mapping field names to required status
        """
        field_requirements = {}
        
        for field in fields:
            # Special handling for certain model types
            if 'DatasetRow' in class_name or 'DatasetResponse' in class_name:
                # Dataset models often have more optional fields
                if field in ['description', 'relatedInformation', 'amendmentFlag']:
                    field_requirements[field] = False
                else:
                    field_requirements[field] = self.analyze_field_name(field)
            elif 'Response' in class_name:
                # Response models might have more required fields
                field_requirements[field] = self.analyze_field_name(field)
            else:
                # Default analysis
                field_requirements[field] = self.analyze_field_name(field)
        
        return field_requirements
    
    def generate_improved_models(self, models_file: Path) -> str:
        """
        Generate improved models with better required field detection.
        
        Args:
            models_file: Path to the current models file
            
        Returns:
            Improved models code
        """
        with open(models_file, 'r') as f:
            content = f.read()
        
        # Parse existing models to extract field information
        import ast
        
        # Simple parsing to extract class and field information
        lines = content.split('\n')
        improved_lines = []
        current_class = None
        current_fields = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Detect class definition
            if line.startswith('class ') and '(' in line:
                current_class = line.split()[1].split('(')[0]
                improved_lines.append(lines[i])
                i += 1
                
                # Skip docstring and config
                while i < len(lines) and (lines[i].strip().startswith('"""') or 
                                         'model_config' in lines[i] or
                                         lines[i].strip() == ''):
                    improved_lines.append(lines[i])
                    i += 1
                
                # Parse fields
                current_fields = []
                while i < len(lines) and lines[i].startswith('    ') and not lines[i].startswith('    class '):
                    field_line = lines[i].strip()
                    if field_line and not field_line.startswith('#'):
                        # Extract field name
                        if ':' in field_line:
                            field_name = field_line.split(':')[0].strip()
                            current_fields.append(field_name)
                    improved_lines.append(lines[i])
                    i += 1
                
                # Apply improved requirements to the fields we just processed
                if current_fields:
                    requirements = self.analyze_model(current_class, current_fields)
                    
                    # Go back and fix the field lines we just added
                    field_start_idx = len(improved_lines) - len(current_fields)
                    for j, field_name in enumerate(current_fields):
                        line_idx = field_start_idx + j
                        if line_idx < len(improved_lines):
                            original_line = improved_lines[line_idx]
                            if requirements.get(field_name, True):  # Default to required
                                # Make field required (remove Optional and default=None)
                                improved_line = original_line.replace('Optional[', '').replace(']', '')
                                if '= None' in improved_line:
                                    improved_line = improved_line.replace('= None', '')
                                if '= Field(default=None' in improved_line:
                                    improved_line = improved_line.replace('= Field(default=None, ', '= Field(')
                                    if improved_line.endswith(')'):
                                        improved_line = improved_line[:-1]
                                improved_lines[line_idx] = improved_line
                
                current_class = None
                current_fields = []
            else:
                improved_lines.append(lines[i])
                i += 1
        
        return '\n'.join(improved_lines)


def main():
    """Main entry point."""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "Model Requirements Analyzer" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    # Find the models file
    script_dir = Path(__file__).parent
    models_file = script_dir.parent / "elexon_bmrs" / "generated_models.py"
    
    if not models_file.exists():
        print(f"✗ Models file not found: {models_file}")
        return 1
    
    print(f"Analyzing models file: {models_file}")
    
    # Analyze and improve models
    analyzer = ModelRequirementAnalyzer()
    improved_content = analyzer.generate_improved_models(models_file)
    
    # Save improved models
    backup_file = models_file.with_suffix('.py.backup')
    print(f"Creating backup: {backup_file}")
    models_file.rename(backup_file)
    
    print(f"Saving improved models: {models_file}")
    with open(models_file, 'w') as f:
        f.write(improved_content)
    
    print("✓ Model requirements improved!")
    print("\nChanges made:")
    print("  - Made core identification fields required (dataset, documentId, etc.)")
    print("  - Made time fields required (publishTime, settlementDate, etc.)")
    print("  - Made data fields required (quantity, generation, demand, etc.)")
    print("  - Kept flag and optional metadata fields as optional")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
