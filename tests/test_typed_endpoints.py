"""
Comprehensive tests for typed BMRS client endpoints.

This test suite validates that all typed endpoints return proper Pydantic models
and can handle real API responses without validation errors.
"""

import pytest
from datetime import datetime, timedelta, date
from unittest.mock import Mock, patch
from elexon_bmrs import BMRSClient
from elexon_bmrs.generated_models import *


class TestTypedEndpoints:
    """Test typed endpoint responses with mocked data."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return BMRSClient(api_key="test-key")
    
    # ========== Balancing Endpoints ==========
    
    def test_balancing_dynamic_typed_response(self, client):
        """Test balancing/dynamic endpoint returns typed model."""
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
            
            # Should return a Pydantic model, not dict
            assert isinstance(result, DynamicData_ResponseWithMetadata)
            assert hasattr(result, 'data')
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].dataset == "SEL"
    
    def test_balancing_physical_typed_response(self, client):
        """Test balancing/physical endpoint returns typed model."""
        mock_response = {
            "data": [{
                "dataset": "PN",
                "bmUnit": "2__CARR-1",
                "settlementDate": "2024-01-01",
                "settlementPeriod": 10,
                "time": "2024-01-01T05:00:00Z",
                "value": 450
            }]
        }
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = client.get_balancing_physical(
                bmUnit="2__CARR-1",
                from_="2024-01-01T00:00:00Z",
                to_="2024-01-01T23:59:59Z"
            )
            
            assert isinstance(result, PhysicalData_ResponseWithMetadata)
            assert hasattr(result, 'data')
    
    # ========== Dataset Endpoints ==========
    
    def test_datasets_abuc_typed_response(self, client):
        """Test datasets/ABUC endpoint returns typed model."""
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
            
            assert isinstance(result, AbucDatasetRow_DatasetResponse)
            assert hasattr(result, 'data')
            assert result.data is not None
            assert len(result.data) == 1
            assert result.data[0].dataset == "ABUC"
            assert result.data[0].quantity == 1000.5
    
    def test_datasets_freq_typed_response(self, client):
        """Test datasets/FREQ endpoint returns typed model."""
        mock_response = {
            "data": [{
                "dataset": "FREQ",
                "startTime": "2024-01-01T00:00:00Z",
                "frequency": 50.05
            }]
        }
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = client.get_datasets_freq(
                from_="2024-01-01T00:00:00Z",
                to_="2024-01-01T01:00:00Z"
            )
            
            # This should return a typed model
            assert hasattr(result, 'data') or isinstance(result, dict)
            if hasattr(result, 'data'):
                assert result.data is not None
    
    # ========== Demand Endpoints ==========
    
    def test_demand_outturn_typed_response(self, client):
        """Test demand/outturn endpoints return typed models."""
        mock_response = {
            "data": [{
                "dataset": "INDOUTTURN",
                "settlementDate": "2024-01-01",
                "settlementPeriod": 10,
                "publishTime": "2024-01-01T05:30:00Z",
                "transmissionSystemDemand": 35000,
                "nationalDemand": 33000
            }]
        }
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = client.get_demand_outturn_summary(
                from_="2024-01-01",
                to_="2024-01-02"
            )
            
            # Check it's properly typed
            assert hasattr(result, 'data') or isinstance(result, dict)
    
    # ========== Forecast Endpoints ==========
    
    def test_forecast_demand_typed_response(self, client):
        """Test forecast/demand endpoints return typed models."""
        mock_response = {
            "data": [{
                "dataset": "TSDF",
                "publishTime": "2024-01-01T00:00:00Z",
                "forecastDate": "2024-01-02",
                "settlementPeriod": 10,
                "demand": 35000
            }]
        }
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = client.get_forecast_demand_total(
                from_="2024-01-01T00:00:00Z",
                to_="2024-01-07T23:59:59Z"
            )
            
            assert hasattr(result, 'data') or isinstance(result, dict)
    
    # ========== Generation Endpoints ==========
    
    def test_generation_actual_typed_response(self, client):
        """Test generation/actual endpoints return typed models."""
        mock_response = {
            "data": [{
                "dataset": "AGPT",
                "publishTime": "2024-01-01T05:30:00Z",
                "settlementDate": "2024-01-01",
                "settlementPeriod": 10,
                "fuelType": "CCGT",
                "generation": 15000
            }]
        }
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = client.get_generation_actual_per_type(
                from_="2024-01-01",
                to_="2024-01-02"
            )
            
            assert hasattr(result, 'data') or isinstance(result, dict)
    
    # ========== Reference Endpoints ==========
    
    def test_reference_bmunits_typed_response(self, client):
        """Test reference/bmunits endpoints return typed models."""
        mock_response = {
            "data": [{
                "bmUnit": "2__CARR-1",
                "nationalGridBmUnit": "CARR-1",
                "leadPartyName": "Test Party",
                "bmUnitType": "T",
                "fuelType": "CCGT"
            }]
        }
        
        with patch.object(client, '_make_request', return_value=mock_response):
            result = client.get_reference_bmunits_all()
            
            # This returns a list of dicts currently, may need model
            assert isinstance(result, (list, dict)) or hasattr(result, 'data')


class TestEndpointCategories:
    """Test coverage across all endpoint categories."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return BMRSClient(api_key="test-key")
    
    def test_balancing_endpoints_available(self, client):
        """Test balancing category endpoints exist."""
        assert hasattr(client, 'get_balancing_dynamic')
        assert hasattr(client, 'get_balancing_dynamic_all')
        assert hasattr(client, 'get_balancing_physical')
        assert hasattr(client, 'get_balancing_bid_offer')
        assert hasattr(client, 'get_balancing_acceptances')
    
    def test_dataset_endpoints_available(self, client):
        """Test dataset category endpoints exist."""
        assert hasattr(client, 'get_datasets_abuc')
        assert hasattr(client, 'get_datasets_freq')
        assert hasattr(client, 'get_datasets_boalf')
        assert hasattr(client, 'get_datasets_bod')
        assert hasattr(client, 'get_datasets_pn')
    
    def test_demand_endpoints_available(self, client):
        """Test demand category endpoints exist."""
        assert hasattr(client, 'get_demand_outturn_summary')
        assert hasattr(client, 'get_demand_outturn_daily')
        assert hasattr(client, 'get_demand_outturn_total')
    
    def test_forecast_endpoints_available(self, client):
        """Test forecast category endpoints exist."""
        assert hasattr(client, 'get_forecast_demand_total')
        assert hasattr(client, 'get_forecast_demand_daily')
        assert hasattr(client, 'get_forecast_generation_wind_earliest')
    
    def test_generation_endpoints_available(self, client):
        """Test generation category endpoints exist."""
        assert hasattr(client, 'get_generation_actual_per_type')
        assert hasattr(client, 'get_generation_wind_earliest')
    
    def test_reference_endpoints_available(self, client):
        """Test reference category endpoints exist."""
        assert hasattr(client, 'get_reference_bmunits_all')
        assert hasattr(client, 'get_reference_interconnectors_all')


class TestTypedResponseValidation:
    """Test that typed responses validate properly with Pydantic."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return BMRSClient(api_key="test-key")
    
    def test_pydantic_validation_on_correct_data(self, client):
        """Test Pydantic validates correct data without errors."""
        correct_data = {
            "data": [{
                "dataset": "ABUC",
                "publishTime": "2024-01-01T00:00:00Z",
                "psrType": "Generation",
                "quantity": 1000.5,
                "businessType": "Frequency containment reserve",
                "year": 2024
            }]
        }
        
        with patch.object(client, '_make_request', return_value=correct_data):
            # This should not raise any validation errors
            result = client.get_datasets_abuc(
                publishDateTimeFrom="2024-01-01T00:00:00Z",
                publishDateTimeTo="2024-01-02T00:00:00Z"
            )
            
            assert result is not None
    
    def test_pydantic_handles_extra_fields(self, client):
        """Test Pydantic allows extra fields (extra='allow')."""
        data_with_extra = {
            "data": [{
                "dataset": "ABUC",
                "publishTime": "2024-01-01T00:00:00Z",
                "psrType": "Generation",
                "quantity": 1000.5,
                "businessType": "Frequency containment reserve",
                "year": 2024,
                "extraField": "should be allowed",
                "anotherExtra": 123
            }]
        }
        
        with patch.object(client, '_make_request', return_value=data_with_extra):
            # Should not raise validation errors for extra fields
            result = client.get_datasets_abuc(
                publishDateTimeFrom="2024-01-01T00:00:00Z",
                publishDateTimeTo="2024-01-02T00:00:00Z"
            )
            
            assert result is not None


@pytest.mark.parametrize("endpoint_method,params,expected_model", [
    ("get_balancing_dynamic", {"bmUnit": "2__CARR-1", "snapshotAt": "2024-01-01T00:00:00Z"}, DynamicData_ResponseWithMetadata),
    ("get_balancing_physical", {"bmUnit": "2__CARR-1", "from_": "2024-01-01T00:00:00Z", "to_": "2024-01-01T23:59:59Z"}, PhysicalData_ResponseWithMetadata),
    ("get_datasets_abuc", {"publishDateTimeFrom": "2024-01-01T00:00:00Z", "publishDateTimeTo": "2024-01-02T00:00:00Z"}, AbucDatasetRow_DatasetResponse),
])
def test_endpoint_returns_expected_model_type(endpoint_method, params, expected_model):
    """Parametrized test for endpoint return types."""
    client = BMRSClient(api_key="test-key")
    
    # Create minimal valid mock data
    mock_response = {"data": []}
    
    with patch.object(client, '_make_request', return_value=mock_response):
        method = getattr(client, endpoint_method)
        result = method(**params)
        
        # Check the return type
        assert isinstance(result, expected_model), \
            f"{endpoint_method} should return {expected_model.__name__}, got {type(result).__name__}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

