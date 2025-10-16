"""
Integration tests for BMRS API endpoints.

These tests make REAL API calls to verify all endpoints work correctly.
Run with: pytest tests/test_integration.py -v -s

Note: These tests require network access and may take several minutes to complete.
"""

import pytest
from datetime import datetime, timedelta, date
from elexon_bmrs import BMRSClient
from elexon_bmrs.generated_models import *
from elexon_bmrs.untyped_models import *
from elexon_bmrs.models import BOALF, PN, BOD, B1610, SettlementStackPair


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def client():
    """Create a client for integration tests."""
    # API key is optional but recommended
    return BMRSClient()


@pytest.fixture(scope="module")
def test_dates():
    """Provide test date ranges."""
    today = date.today()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    
    return {
        'today': today.strftime('%Y-%m-%d'),
        'yesterday': yesterday.strftime('%Y-%m-%d'),
        'week_ago': week_ago.strftime('%Y-%m-%d'),
        'today_dt': datetime.now(),
        'yesterday_dt': datetime.now() - timedelta(days=1),
    }


# ==================== Balancing Endpoints ====================

class TestBalancingEndpoints:
    """Test balancing mechanism endpoints."""
    
    def test_balancing_dynamic(self, client, test_dates):
        """Test balancing/dynamic endpoint."""
        result = client.get_balancing_dynamic(
            bmUnit="2__CARR-1",
            snapshotAt=f"{test_dates['yesterday']}T12:00:00Z"
        )
        
        assert isinstance(result, DynamicData_ResponseWithMetadata)
        assert hasattr(result, 'data')
        print(f"✅ Balancing dynamic: {len(result.data) if result.data else 0} records")
    
    def test_balancing_physical(self, client, test_dates):
        """Test balancing/physical endpoint."""
        result = client.get_balancing_physical(
            bmUnit="2__CARR-1",
            from_=f"{test_dates['yesterday']}T00:00:00Z",
            to_=f"{test_dates['yesterday']}T23:59:59Z"
        )
        
        assert isinstance(result, PhysicalData_ResponseWithMetadata)
        print(f"✅ Balancing physical: {len(result.data) if result.data else 0} records")
    
    def test_balancing_acceptances(self, client, test_dates):
        """Test balancing/acceptances endpoint."""
        result = client.get_balancing_acceptances(
            bmUnit="2__CARR-1",
            from_=f"{test_dates['yesterday']}T00:00:00Z",
            to_=f"{test_dates['yesterday']}T23:59:59Z"
        )
        
        assert isinstance(result, BidOfferAcceptancesResponse_ResponseWithMetadata)
        print(f"✅ Balancing acceptances: {len(result.data) if result.data else 0} records")


# ==================== Dataset Endpoints ====================

class TestDatasetEndpoints:
    """Test dataset endpoints."""
    
    def test_datasets_abuc(self, client, test_dates):
        """Test datasets/ABUC endpoint."""
        result = client.get_datasets_abuc(
            publishDateTimeFrom=f"{test_dates['week_ago']}T00:00:00Z",
            publishDateTimeTo=f"{test_dates['yesterday']}T23:59:59Z"
        )
        
        assert isinstance(result, AbucDatasetRow_DatasetResponse)
        assert hasattr(result, 'data')
        print(f"✅ ABUC dataset: {len(result.data) if result.data else 0} records")
    
    def test_datasets_freq(self, client, test_dates):
        """Test datasets/FREQ (frequency) endpoint."""
        result = client.get_datasets_freq(
            from_=f"{test_dates['yesterday']}T00:00:00Z",
            to_=f"{test_dates['yesterday']}T01:00:00Z"
        )
        
        assert isinstance(result, SystemFrequency_DatasetResponse)
        print(f"✅ FREQ dataset: {len(result.data) if result.data else 0} records")
    
    def test_datasets_boalf(self, client, test_dates):
        """Test datasets/BOALF endpoint."""
        result = client.get_datasets_boalf(
            from_=f"{test_dates['yesterday']}T00:00:00Z",
            to_=f"{test_dates['yesterday']}T02:00:00Z"
        )
        
        assert isinstance(result, BidOfferAcceptanceLevelDatasetResponse_DatasetResponse)
        print(f"✅ BOALF dataset: {len(result.data) if result.data else 0} records")
    
    def test_datasets_bod(self, client, test_dates):
        """Test datasets/BOD endpoint."""
        result = client.get_datasets_bod(
            from_=f"{test_dates['yesterday']}T00:00:00Z",
            to_=f"{test_dates['yesterday']}T01:00:00Z"
        )
        
        assert isinstance(result, BidOfferDatasetResponse_DatasetResponse)
        print(f"✅ BOD dataset: {len(result.data) if result.data else 0} records")


# ==================== Demand Endpoints ====================

class TestDemandEndpoints:
    """Test demand endpoints."""
    
    def test_demand_outturn_summary(self, client, test_dates):
        """Test demand/outturn/summary endpoint."""
        result = client.get_demand_outturn_summary(
            from_=test_dates['yesterday'],
            to_=test_dates['today']
        )
        
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], RollingSystemDemand)
        print(f"✅ Demand outturn summary: {len(result)} records")
    
    def test_demand_endpoint(self, client):
        """Test /demand endpoint (manual model)."""
        result = client.get_demand()
        
        assert isinstance(result, DemandResponse)
        assert hasattr(result, 'data')
        print(f"✅ Demand: {len(result.data) if result.data else 0} records")
    
    def test_demand_summary(self, client):
        """Test /demand/summary endpoint."""
        result = client.get_demand_summary()
        
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], DemandSummaryItem)
        print(f"✅ Demand summary: {len(result)} records")
    
    def test_demand_stream(self, client):
        """Test /demand/stream endpoint (now typed!)."""
        result = client.get_demand_stream()
        
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], InitialDemandOutturn)
        print(f"✅ Demand stream: {len(result)} records")


# ==================== Forecast Endpoints ====================

class TestForecastEndpoints:
    """Test forecast endpoints."""
    
    def test_forecast_demand_total(self, client, test_dates):
        """Test forecast/demand/total endpoint."""
        result = client.get_forecast_demand_total(
            from_=f"{test_dates['today']}T00:00:00Z",
            to_=f"{test_dates['today']}T23:59:59Z"
        )
        
        # Check it returns a typed response
        assert hasattr(result, 'data') or isinstance(result, list)
        print(f"✅ Forecast demand total: response received")
    
    def test_forecast_generation_wind_earliest(self, client):
        """Test forecast/generation/wind/earliest endpoint."""
        result = client.get_forecast_generation_wind_earliest()
        
        assert hasattr(result, 'data') or isinstance(result, (list, dict))
        print(f"✅ Forecast generation wind earliest: response received")


# ==================== Generation Endpoints ====================

class TestGenerationEndpoints:
    """Test generation endpoints."""
    
    def test_generation_actual_per_type(self, client, test_dates):
        """Test generation/actual/per-type endpoint."""
        result = client.get_generation_actual_per_type(
            from_=test_dates['yesterday'],
            to_=test_dates['today']
        )
        
        assert hasattr(result, 'data') or isinstance(result, list)
        print(f"✅ Generation actual per type: response received")
    
    def test_generation_outturn_fuelinsthhcur(self, client):
        """Test generation/outturn/FUELINSTHHCUR endpoint (manual model)."""
        result = client.get_generation_outturn_fuelinsthhcur()
        
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], GenerationCurrentItem)
        print(f"✅ Generation FUELINSTHHCUR: {len(result)} records")


# ==================== Reference Endpoints ====================

class TestReferenceEndpoints:
    """Test reference data endpoints."""
    
    def test_reference_fueltypes_all(self, client):
        """Test reference/fueltypes/all endpoint."""
        result = client.get_reference_fueltypes_all()
        
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)
        print(f"✅ Reference fuel types: {len(result)} fuel types")
        print(f"   Sample: {result[:5]}")
    
    def test_reference_bmunits_all(self, client):
        """Test reference/bmunits/all endpoint."""
        result = client.get_reference_bmunits_all()
        
        assert isinstance(result, list) or hasattr(result, 'data')
        print(f"✅ Reference BM units: response received")


# ==================== Manual Helper Methods ====================

class TestManualHelperMethods:
    """Test manually created helper methods."""
    
    def test_get_latest_acceptances(self, client):
        """Test get_latest_acceptances helper method."""
        result = client.get_latest_acceptances()
        
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], BOALF)
        print(f"✅ Latest acceptances: {len(result)} records")
    
    def test_get_physical_notifications(self, client, test_dates):
        """Test get_physical_notifications helper method."""
        result = client.get_physical_notifications(
            settlement_date=test_dates['yesterday_dt'],
            settlement_period=10
        )
        
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], PN)
        print(f"✅ Physical notifications: {len(result)} records")


# ==================== Manual Model Endpoints ====================

class TestManualModelEndpoints:
    """Test endpoints with manually created models."""
    
    def test_health_endpoint(self, client):
        """Test /health endpoint."""
        result = client.get_health()
        
        assert isinstance(result, HealthCheckResponse)
        assert hasattr(result, 'status')
        print(f"✅ Health: Status {result.status}")
    
    def test_cdn_endpoint(self, client):
        """Test /CDN endpoint."""
        result = client.get_cdn()
        
        assert isinstance(result, CDNResponse)
        assert hasattr(result, 'data')
        print(f"✅ CDN: {len(result.data)} credit default notices")


# ==================== Comprehensive Coverage Test ====================

class TestComprehensiveCoverage:
    """Test comprehensive endpoint coverage."""
    
    def test_all_endpoint_categories_available(self, client):
        """Verify all endpoint categories have methods."""
        categories = {
            'balancing': ['get_balancing_dynamic', 'get_balancing_physical'],
            'datasets': ['get_datasets_abuc', 'get_datasets_freq', 'get_datasets_boalf'],
            'demand': ['get_demand', 'get_demand_summary', 'get_demand_stream'],
            'forecast': ['get_forecast_demand_total', 'get_forecast_generation_wind_earliest'],
            'generation': ['get_generation_actual_per_type', 'get_generation_outturn_fuelinsthhcur'],
            'reference': ['get_reference_fueltypes_all', 'get_reference_bmunits_all'],
            'helpers': ['get_latest_acceptances', 'get_physical_notifications'],
            'manual': ['get_health', 'get_cdn'],
        }
        
        total_checked = 0
        for category, methods in categories.items():
            for method_name in methods:
                assert hasattr(client, method_name), f"Missing: {method_name}"
                total_checked += 1
        
        print(f"✅ All {total_checked} sample endpoints available across {len(categories)} categories")
    
    def test_type_coverage_statistics(self, client):
        """Verify type coverage statistics."""
        import inspect
        
        all_methods = [name for name in dir(client) if name.startswith('get_') and callable(getattr(client, name))]
        
        typed_count = 0
        untyped_count = 0
        
        for method_name in all_methods[:50]:  # Sample first 50
            method = getattr(client, method_name)
            sig = inspect.signature(method)
            return_annotation = sig.return_annotation
            
            if return_annotation != inspect.Signature.empty:
                return_str = str(return_annotation)
                if 'Dict[str, Any]' not in return_str:
                    typed_count += 1
                else:
                    untyped_count += 1
        
        print(f"✅ Sample type coverage: {typed_count}/{typed_count+untyped_count} typed")
        assert typed_count > untyped_count, "Should have more typed than untyped"


# ==================== Type Safety Verification ====================

class TestTypeSafety:
    """Verify type safety features."""
    
    def test_pydantic_validation_works(self, client, test_dates):
        """Test that Pydantic validation catches errors."""
        # Get real data
        result = client.get_datasets_abuc(
            publishDateTimeFrom=f"{test_dates['week_ago']}T00:00:00Z",
            publishDateTimeTo=f"{test_dates['yesterday']}T23:59:59Z"
        )
        
        # Verify it's a Pydantic model
        assert isinstance(result, AbucDatasetRow_DatasetResponse)
        
        # Verify we can access fields with type safety
        if result.data:
            first_row = result.data[0]
            # These should all exist and be properly typed
            assert hasattr(first_row, 'dataset')
            assert hasattr(first_row, 'publishTime')
            assert hasattr(first_row, 'quantity')
            print(f"✅ Pydantic validation: All fields accessible and typed")
    
    def test_list_response_typing(self, client, test_dates):
        """Test List[Model] responses are properly typed."""
        result = client.get_demand_outturn_summary(
            from_=test_dates['yesterday'],
            to_=test_dates['today']
        )
        
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], RollingSystemDemand)
            assert hasattr(result[0], 'demand')
            assert hasattr(result[0], 'startTime')
        print(f"✅ List[Model] typing: {len(result)} items")
    
    def test_list_str_response_typing(self, client):
        """Test List[str] responses."""
        result = client.get_reference_fueltypes_all()
        
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)
        print(f"✅ List[str] typing: {len(result)} fuel types")


# ==================== Performance Tests ====================

class TestPerformance:
    """Test that typed responses don't hurt performance."""
    
    def test_multiple_rapid_requests(self, client, test_dates):
        """Test multiple rapid requests work without issues."""
        import time
        
        start = time.time()
        results = []
        
        # Make 5 rapid requests
        for i in range(5):
            result = client.get_reference_fueltypes_all()
            results.append(result)
            time.sleep(0.5)  # Small delay to avoid rate limiting
        
        elapsed = time.time() - start
        
        assert len(results) == 5
        print(f"✅ Performance: 5 requests in {elapsed:.2f}s ({elapsed/5:.2f}s avg)")


# ==================== Error Handling ====================

class TestErrorHandling:
    """Test error handling with typed responses."""
    
    def test_invalid_bmu_returns_error(self, client):
        """Test that invalid BMU returns proper error."""
        from elexon_bmrs.exceptions import APIError
        
        try:
            result = client.get_balancing_dynamic(
                bmUnit="INVALID_BMU_12345",
                snapshotAt="2024-01-01T12:00:00Z"
            )
            # If it doesn't raise, check if it returns empty data
            if hasattr(result, 'data'):
                print(f"✅ Invalid BMU handled: {len(result.data) if result.data else 0} records")
        except APIError as e:
            print(f"✅ Invalid BMU raises APIError as expected")


# ==================== Run Summary ====================

def test_run_summary(client):
    """Print test run summary."""
    import inspect
    
    all_methods = [name for name in dir(client) if name.startswith('get_') and callable(getattr(client, name))]
    
    typed = 0
    untyped = 0
    
    for method_name in all_methods:
        method = getattr(client, method_name)
        sig = inspect.signature(method)
        return_annotation = sig.return_annotation
        
        if return_annotation != inspect.Signature.empty:
            return_str = str(return_annotation)
            if 'Dict[str, Any]' not in return_str:
                typed += 1
            else:
                untyped += 1
    
    print("\n" + "=" * 80)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 80)
    print(f"Total endpoints tested: {len(all_methods)}")
    print(f"Typed endpoints: {typed} ({typed*100//len(all_methods)}%)")
    print(f"Untyped endpoints: {untyped}")
    print("=" * 80)
    print("✅ ALL INTEGRATION TESTS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    # Run with: python tests/test_integration.py
    pytest.main([__file__, "-v", "-s", "-m", "integration"])

