"""Tests for the BMRS client."""

import pytest
from datetime import date, datetime
from unittest.mock import Mock, patch

from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)


class TestBMRSClient:
    """Test suite for BMRSClient."""

    def test_client_initialization(self):
        """Test client initialization with default parameters."""
        client = BMRSClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.timeout == 30
        assert client.verify_ssl is True

    def test_client_custom_config(self):
        """Test client initialization with custom configuration."""
        client = BMRSClient(
            api_key="test-key",
            base_url="https://custom.api.com",
            timeout=60,
            verify_ssl=False,
        )
        assert client.base_url == "https://custom.api.com"
        assert client.timeout == 60
        assert client.verify_ssl is False

    def test_context_manager(self):
        """Test client can be used as context manager."""
        with BMRSClient(api_key="test-key") as client:
            assert client.api_key == "test-key"

    def test_format_date_string(self):
        """Test date formatting from string."""
        client = BMRSClient(api_key="test-key")
        formatted = client._format_date("2024-01-15")
        assert formatted == "2024-01-15"

    def test_format_date_object(self):
        """Test date formatting from date object."""
        client = BMRSClient(api_key="test-key")
        test_date = date(2024, 1, 15)
        formatted = client._format_date(test_date)
        assert formatted == "2024-01-15"

    def test_format_datetime_object(self):
        """Test date formatting from datetime object."""
        client = BMRSClient(api_key="test-key")
        test_datetime = datetime(2024, 1, 15, 10, 30)
        formatted = client._format_date(test_datetime)
        assert formatted == "2024-01-15"

    def test_validate_settlement_period_valid(self):
        """Test settlement period validation with valid values."""
        client = BMRSClient(api_key="test-key")
        # Should not raise any exception
        client._validate_settlement_period(1)
        client._validate_settlement_period(25)
        client._validate_settlement_period(50)

    def test_validate_settlement_period_invalid(self):
        """Test settlement period validation with invalid values."""
        client = BMRSClient(api_key="test-key")

        with pytest.raises(ValidationError):
            client._validate_settlement_period(0)

        with pytest.raises(ValidationError):
            client._validate_settlement_period(51)

        with pytest.raises(ValidationError):
            client._validate_settlement_period(-1)

    @patch("elexon_bmrs.client.requests.Session.request")
    def test_authentication_error(self, mock_request):
        """Test authentication error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response

        client = BMRSClient(api_key="invalid-key")

        with pytest.raises(AuthenticationError):
            client.get_system_demand(from_date=date.today(), to_date=date.today())

    @patch("elexon_bmrs.client.requests.Session.request")
    def test_rate_limit_error(self, mock_request):
        """Test rate limit error handling."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_request.return_value = mock_response

        client = BMRSClient(api_key="test-key")

        with pytest.raises(RateLimitError) as exc_info:
            client.get_system_demand(from_date=date.today(), to_date=date.today())

        assert exc_info.value.retry_after == 60

    @patch("elexon_bmrs.client.requests.Session.request")
    def test_api_error(self, mock_request):
        """Test generic API error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.json.return_value = {"error": "Server error"}
        mock_request.return_value = mock_response

        client = BMRSClient(api_key="test-key")

        with pytest.raises(APIError) as exc_info:
            client.get_system_demand(from_date=date.today(), to_date=date.today())

        assert exc_info.value.status_code == 500

    @patch("elexon_bmrs.client.requests.Session.request")
    def test_successful_request(self, mock_request):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{
                "settlementDate": "2024-01-15",
                "settlementPeriod": 10,
                "demand": 35000,
                "publishTime": "2024-01-15T10:00:00Z",
                "startTime": "2024-01-15T04:30:00Z"
            }]
        }
        mock_request.return_value = mock_response

        client = BMRSClient(api_key="test-key")
        result = client.get_system_demand(from_date=date.today(), to_date=date.today())

        # Result can be either dict or Pydantic model depending on client implementation
        if hasattr(result, 'data'):
            # Pydantic model
            assert result.data is not None
            assert len(result.data) == 1
        else:
            # Dict
            assert "data" in result
            assert len(result["data"]) == 1

    @patch("elexon_bmrs.client.requests.Session.request")
    def test_get_generation_by_fuel_type(self, mock_request):
        """Test get_generation_by_fuel_type method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{
                "fuelType": "WIND",
                "generation": 5000,
                "publishTime": "2024-01-15T10:00:00Z",
                "startTime": "2024-01-15T04:30:00Z",
                "settlementDate": "2024-01-15",
                "settlementPeriod": 10
            }]
        }
        mock_request.return_value = mock_response

        client = BMRSClient(api_key="test-key")
        result = client.get_generation_by_fuel_type(
            from_date="2024-01-01",
            to_date="2024-01-02",
            settlement_period_from=1,
            settlement_period_to=48,
        )

        # Result can be either dict or Pydantic model depending on client implementation
        if hasattr(result, 'data'):
            # Pydantic model
            assert result.data is not None
            assert len(result.data) == 1
        else:
            # Dict
            assert "data" in result
            assert len(result["data"]) == 1
            assert result["data"][0]["fuelType"] == "WIND"
        # Verify the request was made with correct parameters
        call_args = mock_request.call_args
        assert call_args[1]["params"]["FromSettlementDate"] == "2024-01-01"
        assert call_args[1]["params"]["ToSettlementDate"] == "2024-01-02"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

