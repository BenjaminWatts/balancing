"""Tests for custom exceptions."""

import pytest
from elexon_bmrs.exceptions import (
    BMRSException,
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)


class TestExceptions:
    """Test suite for custom exceptions."""

    def test_bmrs_exception(self):
        """Test base BMRSException."""
        exc = BMRSException("Test error")
        assert str(exc) == "Test error"
        assert isinstance(exc, Exception)

    def test_api_error(self):
        """Test APIError with status code and response."""
        exc = APIError("API failed", status_code=500, response={"error": "Server error"})
        assert str(exc) == "API failed"
        assert exc.status_code == 500
        assert exc.response == {"error": "Server error"}

    def test_authentication_error(self):
        """Test AuthenticationError."""
        exc = AuthenticationError("Invalid credentials")
        assert str(exc) == "Invalid credentials"
        assert isinstance(exc, BMRSException)

    def test_rate_limit_error(self):
        """Test RateLimitError with retry_after."""
        exc = RateLimitError("Rate limit exceeded", retry_after=60)
        assert str(exc) == "Rate limit exceeded"
        assert exc.retry_after == 60

    def test_validation_error(self):
        """Test ValidationError."""
        exc = ValidationError("Invalid input")
        assert str(exc) == "Invalid input"
        assert isinstance(exc, BMRSException)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


