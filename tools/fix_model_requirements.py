"""
Fix model requirements by making commonly required fields non-optional.

This script makes targeted improvements to the generated models by identifying
fields that should be required based on BMRS API patterns.
"""

import re
from pathlib import Path


def fix_model_requirements(content: str) -> str:
    """
    Fix model requirements by making key fields required.
    
    Args:
        content: The current model file content
        
    Returns:
        Improved content with better field requirements
    """
    lines = content.split('\n')
    improved_lines = []
    
    # Fields that should be required (non-optional)
    required_fields = {
        # Core identification
        'dataset', 'documentId', 'publishTime', 'settlementDate', 'settlementPeriod',
        
        # Time fields
        'startTime', 'endTime', 'timeFrom', 'timeTo', 'measurementTime',
        'createdDateTime', 'messageReceivedDateTime', 'halfHourEndTime',
        
        # BM Unit identification  
        'bmUnit', 'nationalGridBmUnit', 'nationalGridBmUnitId',
        
        # Core data
        'quantity', 'generation', 'demand', 'price', 'cost', 'volume',
        
        # Status and types
        'businessType', 'psrType', 'fuelType', 'status', 'messageType',
        
        # IDs
        'id', 'mrid', 'acceptanceNumber', 'pairId', 'timeSeriesId',
        'documentRevisionNumber', 'acceptanceId',
        
        # Other commonly required fields
        'participantId', 'participantName', 'flowDirection', 'marketAgreementType',
        'processType', 'contractIdentification', 'tradeDirection', 'tradeQuantity',
        'tradePrice', 'traderUnit', 'warningType', 'messageHeading', 'eventType',
        'unavailabilityType', 'assetId', 'assetType', 'affectedUnit', 'biddingZone',
        'normalCapacity', 'eventStatus', 'eventStartTime', 'eventEndTime', 'cause',
        'mRID', 'revisionNumber', 'affectedDso', 'demandControlId', 'instructionSequence',
        'demandControlEventFlag', 'systemManagementActionFlag', 'amendmentFlag',
        'serialNumber', 'fileCreationTime', 'tradingUnitType', 'tradingUnitName',
        'settlementRunType', 'deliveryMode', 'importVolume', 'exportVolume', 'netVolume',
    }
    
    # Fields that should remain optional
    optional_fields = {
        # Descriptions and metadata
        'description', 'relatedInformation', 'messageText', 'warningText',
        'clearedDefaultText', 'url', 'receiverIdentification', 'senderIdentification',
        
        # Flags and indicators
        'deemedBoFlag', 'soFlag', 'storFlag', 'rrFlag', 'activeFlag', 'isTendered',
        'bsadDefaulted', 'creditQualifyingStatus', 'demandInProductionFlag', 'fpnFlag',
        'cadlFlag', 'repricedIndicator', 'interconnector', 'productionOrConsumptionFlag',
        
        # Optional numeric fields
        'percentage', 'ratio', 'multiplier', 'adjustment', 'deratedMargin',
        'halfHourPercentage', 'twentyFourHourPercentage', 'currentPercentage',
        'transmissionLossMultiplier', 'reserveScarcityPrice',
        
        # Optional capacity/limit fields
        'capacity', 'limit', 'minimum', 'maximum', 'available', 'unavailable',
        'availableCapacity', 'unavailableCapacity', 'assetNormalCapacity',
        'workingDayCreditAssessmentImportCapability', 'nonWorkingDayCreditAssessmentImportCapability',
        'workingDayCreditAssessmentExportCapability', 'nonWorkingDayCreditAssessmentExportCapability',
        'demandCapacity', 'generationCapacity', 'installedCapacity',
        
        # Optional time fields
        'durationUncertainty', 'clearedDefaultSettlementDate', 'clearedDefaultSettlementPeriod',
        'enteredDefaultSettlementDate', 'enteredDefaultSettlementPeriod',
        
        # Optional location/area fields
        'area', 'zone', 'boundary', 'region', 'gspGroupId', 'gspGroupName',
        'affectedArea', 'systemZone', 'biddingZone', 'interconnectorName',
        'interconnectorId', 'voltageLimit', 'registeredResourceEicCode', 'registeredResourceName',
        
        # Optional secondary fields
        'secondaryQuantity', 'energyPrice', 'procurementPrice', 'amount',
        'forecastHorizon', 'temperatureReferenceAverage', 'temperatureReferenceHigh',
        'temperatureReferenceLow', 'temperature', 'frequency',
        
        # Optional metadata
        'year', 'month', 'week', 'forecastDate', 'forecastWeek', 'forecastYear',
        'forecastWeekCommencingDate', 'forecastMonth', 'calendarWeekNumber',
        'minimumPossible', 'maximumAvailable', 'weekStartDate',
    }
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for field definitions
        if (line.strip().startswith('#') or 
            'model_config' in line or 
            'class ' in line or
            '"""' in line or
            line.strip() == ''):
            improved_lines.append(line)
            i += 1
            continue
            
        # Check if this looks like a field definition
        if (':' in line and '=' in line and 
            ('Optional[' in line or 'Field(default=None' in line)):
            
            # Extract field name
            field_name = line.split(':')[0].strip()
            
            # Determine if field should be required
            if field_name in required_fields:
                # Make field required
                if 'Optional[' in line:
                    # Remove Optional wrapper
                    new_line = line.replace('Optional[', '').replace(']', '')
                    # Remove default=None
                    if '= None' in new_line:
                        new_line = new_line.replace('= None', '')
                    # Clean up Field parameters
                    if '= Field(default=None' in new_line:
                        new_line = new_line.replace('= Field(default=None, ', '= Field(')
                        # Remove trailing comma and parenthesis if needed
                        if new_line.strip().endswith(')'):
                            new_line = new_line.strip()[:-1]
                    improved_lines.append(new_line)
                else:
                    # Already not Optional, just remove default=None
                    new_line = line.replace('= None', '')
                    if '= Field(default=None' in new_line:
                        new_line = new_line.replace('= Field(default=None, ', '= Field(')
                        if new_line.strip().endswith(')'):
                            new_line = new_line.strip()[:-1]
                    improved_lines.append(new_line)
                    
            elif field_name in optional_fields:
                # Keep as optional
                improved_lines.append(line)
            else:
                # For unknown fields, be conservative and keep as optional
                improved_lines.append(line)
                
        else:
            improved_lines.append(line)
            
        i += 1
    
    return '\n'.join(improved_lines)


def main():
    """Main entry point."""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "Model Requirements Fixer" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    # Find the models file
    script_dir = Path(__file__).parent
    models_file = script_dir.parent / "elexon_bmrs" / "generated_models.py"
    
    if not models_file.exists():
        print(f"✗ Models file not found: {models_file}")
        return 1
    
    print(f"Fixing model requirements in: {models_file}")
    
    # Read current content
    with open(models_file, 'r') as f:
        content = f.read()
    
    # Fix requirements
    improved_content = fix_model_requirements(content)
    
    # Create backup
    backup_file = models_file.with_suffix('.py.backup')
    if not backup_file.exists():
        print(f"Creating backup: {backup_file}")
        with open(backup_file, 'w') as f:
            f.write(content)
    
    # Save improved models
    print(f"Saving improved models: {models_file}")
    with open(models_file, 'w') as f:
        f.write(improved_content)
    
    print("✓ Model requirements fixed!")
    print("\nChanges made:")
    print("  ✓ Made core fields required: dataset, documentId, publishTime, etc.")
    print("  ✓ Made time fields required: startTime, endTime, settlementDate, etc.")  
    print("  ✓ Made data fields required: quantity, generation, demand, price, etc.")
    print("  ✓ Made ID fields required: id, mrid, acceptanceNumber, etc.")
    print("  ✓ Kept metadata fields optional: description, flags, percentages, etc.")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
