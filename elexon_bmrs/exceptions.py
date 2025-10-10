"""Custom exceptions for the Elexon BMRS client."""


class BMRSException(Exception):
    """Base exception for all BMRS client errors."""

    pass


class APIError(BMRSException):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class AuthenticationError(BMRSException):
    """Raised when API authentication fails."""

    pass


class RateLimitError(BMRSException):
    """Raised when API rate limit is exceeded."""

    def __init__(self, message: str, retry_after: int = None):
        self.retry_after = retry_after
        super().__init__(message)


class ValidationError(BMRSException):
    """Raised when input validation fails."""

    pass


