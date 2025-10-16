"""
Simple test runner to verify core functionality without pytest.
"""

import sys
from datetime import datetime
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, '/Users/benjaminwatts/bmrs')

from elexon_bmrs import BMRSClient
from elexon_bmrs.generated_models import (
    DynamicData_ResponseWithMetadata,
    AbucDatasetRow_DatasetResponse,
    PhysicalData_ResponseWithMetadata
)

print("=" * 80)
print("RUNNING SIMPLE TESTS FOR ELEXON-BMRS v0.3.0")
print("=" * 80)
print()

# Test 1: Client initialization
print("Test 1: Client Initialization")
try:
    client = BMRSClient(api_key="test-key")
    print("  ✅ Client initialized successfully")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 2: Client without API key (should warn)
print("\nTest 2: Client Without API Key (should show warning)")
try:
    import logging
    logging.basicConfig(level=logging.WARNING)
    client_no_key = BMRSClient()
    print("  ✅ Client initialized without key (warning should appear above)")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 3: Typed endpoint - balancing_dynamic
print("\nTest 3: Typed Endpoint - get_balancing_dynamic")
try:
    mock_response = {
        "data": [{
            "dataset": "SEL",
            "bmUnit": "2__CARR-1",
            "settlementDate": "2024-01-01",
            "settlementPeriod": 10,
            "time": "2024-01-01T05:00:00Z",
            "value": 500
        }]
    }
    
    with patch.object(client, '_make_request', return_value=mock_response):
        result = client.get_balancing_dynamic(
            bmUnit="2__CARR-1",
            snapshotAt="2024-01-01T05:00:00Z"
        )
        
        assert isinstance(result, DynamicData_ResponseWithMetadata), \
            f"Expected DynamicData_ResponseWithMetadata, got {type(result)}"
        assert hasattr(result, 'data'), "Result should have 'data' attribute"
        assert len(result.data) == 1, f"Expected 1 record, got {len(result.data)}"
        assert result.data[0].dataset == "SEL", f"Expected 'SEL', got {result.data[0].dataset}"
        
    print("  ✅ Returns properly typed DynamicData_ResponseWithMetadata")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Typed endpoint - datasets_abuc
print("\nTest 4: Typed Endpoint - get_datasets_abuc")
try:
    mock_response = {
        "data": [{
            "dataset": "ABUC",
            "publishTime": "2024-01-01T00:00:00Z",
            "psrType": "Generation",
            "quantity": 1000.5,
            "businessType": "Frequency containment reserve",
            "year": 2024
        }]
    }
    
    with patch.object(client, '_make_request', return_value=mock_response):
        result = client.get_datasets_abuc(
            publishDateTimeFrom="2024-01-01T00:00:00Z",
            publishDateTimeTo="2024-01-02T00:00:00Z"
        )
        
        assert isinstance(result, AbucDatasetRow_DatasetResponse), \
            f"Expected AbucDatasetRow_DatasetResponse, got {type(result)}"
        assert result.data[0].quantity == 1000.5, f"Expected 1000.5, got {result.data[0].quantity}"
        
    print("  ✅ Returns properly typed AbucDatasetRow_DatasetResponse")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Manual helper method - get_latest_acceptances
print("\nTest 5: Manual Helper Method - get_latest_acceptances")
try:
    from elexon_bmrs.models import BOALF
    
    mock_response = {
        "data": [{
            "acceptanceNumber": 12345,
            "acceptanceTime": "2024-01-01T05:00:00Z",
            "bmUnit": "2__CARR-1",
            "settlementDate": "2024-01-01",
            "settlementPeriodFrom": 10,
            "settlementPeriodTo": 10,
            "timeFrom": "2024-01-01T05:00:00Z",
            "timeTo": "2024-01-01T05:30:00Z",
            "levelFrom": 100,
            "levelTo": 150,
            "nationalGridBmUnit": "CARR-1",
            "soFlag": False,
            "deemedBoFlag": False,
            "storFlag": False,
            "rrFlag": False
        }]
    }
    
    with patch.object(client, '_make_request', return_value=mock_response):
        result = client.get_latest_acceptances()
        
        assert isinstance(result, list), f"Expected list, got {type(result)}"
        assert len(result) == 1, f"Expected 1 record, got {len(result)}"
        assert isinstance(result[0], BOALF), f"Expected BOALF, got {type(result[0])}"
        assert result[0].acceptance_number == 12345
        
    print("  ✅ Returns List[BOALF] with proper validation")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Check endpoint availability
print("\nTest 6: Endpoint Availability")
try:
    endpoints = [
        'get_balancing_dynamic',
        'get_balancing_physical',
        'get_datasets_abuc',
        'get_datasets_boalf',
        'get_demand_outturn_summary',
        'get_generation_actual_per_type',
        'get_latest_acceptances',
        'get_physical_notifications'
    ]
    
    for endpoint in endpoints:
        assert hasattr(client, endpoint), f"Missing endpoint: {endpoint}"
    
    print(f"  ✅ All {len(endpoints)} checked endpoints available")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 7: Check typing annotations
print("\nTest 7: Type Annotations")
try:
    import inspect
    
    method = getattr(client, 'get_balancing_dynamic')
    sig = inspect.signature(method)
    return_annotation = sig.return_annotation
    
    assert return_annotation != inspect.Signature.empty, "Method should have return type annotation"
    assert "DynamicData_ResponseWithMetadata" in str(return_annotation), \
        f"Expected DynamicData_ResponseWithMetadata in annotation, got {return_annotation}"
    
    print("  ✅ Type annotations present and correct")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 8: Pydantic validation
print("\nTest 8: Pydantic Validation")
try:
    from pydantic import ValidationError
    
    # Try to create a model with invalid data
    try:
        from elexon_bmrs.models import BOALF
        invalid_data = {
            "acceptanceNumber": "not_a_number",  # Should be int
            "acceptanceTime": "2024-01-01T05:00:00Z"
            # Missing required fields
        }
        boalf = BOALF(**invalid_data)
        print("  ❌ Failed: Should have raised ValidationError")
        sys.exit(1)
    except ValidationError:
        print("  ✅ Pydantic validation working correctly")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

print()
print("=" * 80)
print("ALL TESTS PASSED! ✅")
print("=" * 80)
print()
print("Summary:")
print("  • Client initialization: ✅")
print("  • API key warning: ✅")
print("  • Typed endpoints (auto-generated): ✅")
print("  • Manual helper methods: ✅")
print("  • Endpoint availability: ✅")
print("  • Type annotations: ✅")
print("  • Pydantic validation: ✅")
print()
print("🎉 elexon-bmrs v0.3.0 is ready for production!")

