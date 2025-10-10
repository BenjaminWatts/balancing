"""Main BMRS API client."""

import logging
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import requests
from dateutil import parser

from elexon_bmrs.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)
from elexon_bmrs.models import (
    APIResponse,
    TypedAPIResponse,
    SystemDemandResponse,
    GenerationResponse,
    WindForecastResponse,
    SystemPricesResponse,
    SystemFrequencyResponse,
    ImbalancePricesResponse,
)
from elexon_bmrs.generated_client import GeneratedBMRSMethods

logger = logging.getLogger(__name__)


class BMRSClient(GeneratedBMRSMethods):
    """
    Client for interacting with the Elexon BMRS API.

    The Balancing Mechanism Reporting Service (BMRS) provides access to UK electricity
    market data including generation, demand, pricing, and system information.
    
    This client provides access to **287 API endpoints** covering:
    - Balancing Mechanism data (dynamic, physical, bid/offer, acceptances)
    - Generation data (by fuel type, BMU, wind forecasts)
    - Demand data (actual, forecast, transmission, national)
    - Pricing data (system prices, imbalance prices, market index)
    - System data (frequency, warnings, messages)
    - Settlement data (cashflows, volumes, notices)
    - Non-BM data (STOR, DISBSAD, NETBSAD)
    - Transmission data (B1610, BOD, BOALF, etc.)
    - Reference data (CDN, TEMP, UOU, etc.)
    
    All methods are auto-generated from the official OpenAPI specification with full
    docstrings, type hints, and parameter descriptions.

    API Key:
        While the API can function without a key, Elexon strongly recommends using one.
        Benefits of using an API key:
        - Higher rate limits
        - Better performance and reliability
        - Usage tracking and support
        Register for a free API key at: https://www.elexonportal.co.uk/
    
    Rate Limiting:
        The API implements rate limiting. When exceeded, a RateLimitError is raised
        with optional retry_after information. Implement exponential backoff or respect
        the Retry-After header for production use. See examples/advanced_usage.py for
        rate limit handling patterns.

    Args:
        api_key: Your Elexon BMRS API key (optional but strongly recommended)
        base_url: Base URL for the BMRS API (defaults to production)
        timeout: Request timeout in seconds (default: 30)
        verify_ssl: Whether to verify SSL certificates (default: True)
    
    Raises:
        RateLimitError: When API rate limit is exceeded (HTTP 429)
        AuthenticationError: When API key is invalid (HTTP 401)
        APIError: For other API errors (HTTP 4xx/5xx)
        ValidationError: When input parameters are invalid
    
    Example:
        >>> from elexon_bmrs import BMRSClient
        >>> 
        >>> # Initialize client
        >>> client = BMRSClient(api_key="your-key")
        >>> 
        >>> # Common methods with type-safe responses
        >>> demand = client.get_system_demand(from_date="2024-01-01", to_date="2024-01-02")
        >>> generation = client.get_generation_by_fuel_type(from_date="2024-01-01", to_date="2024-01-02")
        >>> prices = client.get_system_prices(settlement_date="2024-01-01", settlement_period=10)
        >>> 
        >>> # Access to all 287 endpoints
        >>> dynamic_data = client.get_balancing_dynamic(bmUnit="2__HFLEX001", snapshotAt="2024-01-01T12:00:00Z")
        >>> acceptances = client.get_balancing_acceptances_all(settlementDate="2024-01-01", settlementPeriod=1)
        >>> 
        >>> # With context manager (recommended)
        >>> with BMRSClient(api_key="your-key") as client:
        ...     data = client.get_system_demand(from_date="2024-01-01", to_date="2024-01-02")
        ...     # Client automatically closed
    
    See Also:
        For a complete list of all 287 available methods, see the API documentation or use:
        >>> dir(client)  # List all available methods
        >>> help(client.get_balancing_dynamic)  # Get help for specific method
    """

    # Official BMRS API base URL
    DEFAULT_BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True,
    ):
        """Initialize the BMRS client."""
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()

        # Warn if no API key is provided
        if not self.api_key:
            logger.warning(
                "⚠️  No API key provided. While the API may work without a key, "
                "Elexon strongly recommends using one for:\n"
                "  • Higher rate limits\n"
                "  • Better performance\n"
                "  • Usage tracking and support\n"
                "Get your free API key at: https://www.elexonportal.co.uk/"
            )

        # Set default headers
        self.session.headers.update(
            {
                "User-Agent": "elexon-bmrs-python/0.1.0",
                "Accept": "application/json",
            }
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the BMRS API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            **kwargs: Additional arguments to pass to requests

        Returns:
            Parsed JSON response

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            APIError: For other API errors
        """
        url = urljoin(self.base_url, endpoint)

        # Add API key to params if provided
        if params is None:
            params = {}
        if self.api_key:
            params["APIKey"] = self.api_key

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs,
            )

            # Handle different status codes
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or authentication failed")
            elif response.status_code == 429:
                # Rate limit exceeded - extract Retry-After header if present
                # The API returns this header indicating when to retry (in seconds)
                retry_after = response.headers.get("Retry-After")
                raise RateLimitError(
                    "API rate limit exceeded. Please reduce request frequency.",
                    retry_after=int(retry_after) if retry_after else None,
                )
            elif response.status_code >= 400:
                raise APIError(
                    f"API request failed: {response.text}",
                    status_code=response.status_code,
                    response=response.json() if response.text else None,
                )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise APIError("Request timeout")
        except requests.exceptions.ConnectionError:
            raise APIError("Connection error")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def _format_date(self, dt: Union[str, date, datetime]) -> str:
        """
        Format date/datetime to string format expected by API.

        Args:
            dt: Date as string, date, or datetime object

        Returns:
            Formatted date string (YYYY-MM-DD)
        """
        if isinstance(dt, str):
            # Try to parse the string to validate it
            dt = parser.parse(dt).date()
        elif isinstance(dt, datetime):
            dt = dt.date()

        return dt.strftime("%Y-%m-%d")

    def _validate_settlement_period(self, period: int) -> None:
        """
        Validate settlement period (1-50, representing half-hour periods in a day).

        Args:
            period: Settlement period number

        Raises:
            ValidationError: If period is invalid
        """
        if not 1 <= period <= 50:
            raise ValidationError("Settlement period must be between 1 and 50")

    # ==================== Market Index Data ====================

    def get_market_index(
        self, settlement_date: Union[str, date], settlement_period: Optional[int] = None
    ) -> SystemPricesResponse:
        """
        Get market index data for a specific settlement date and period.

        Args:
            settlement_date: Settlement date (YYYY-MM-DD)
            settlement_period: Settlement period (1-50), optional

        Returns:
            SystemPricesResponse with market index data
        """
        params = {"SettlementDate": self._format_date(settlement_date)}

        if settlement_period is not None:
            self._validate_settlement_period(settlement_period)
            params["Period"] = settlement_period

        result = self._make_request("GET", "/MID", params=params)
        return SystemPricesResponse(**result)

    # ==================== Generation Data ====================

    def get_generation_by_fuel_type(
        self,
        from_date: Union[str, date],
        to_date: Union[str, date],
        settlement_period_from: Optional[int] = None,
        settlement_period_to: Optional[int] = None,
    ) -> GenerationResponse:
        """
        Get generation data by fuel type.

        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            settlement_period_from: Start settlement period (1-50), optional
            settlement_period_to: End settlement period (1-50), optional

        Returns:
            GenerationResponse with generation data by fuel type
        """
        params = {
            "FromSettlementDate": self._format_date(from_date),
            "ToSettlementDate": self._format_date(to_date),
        }

        if settlement_period_from is not None:
            self._validate_settlement_period(settlement_period_from)
            params["FromSettlementPeriod"] = settlement_period_from

        if settlement_period_to is not None:
            self._validate_settlement_period(settlement_period_to)
            params["ToSettlementPeriod"] = settlement_period_to

        result = self._make_request("GET", "/FUELINST", params=params)
        return GenerationResponse(**result)

    def get_actual_generation_output(
        self, settlement_date: Union[str, date], settlement_period: Optional[int] = None
    ) -> GenerationResponse:
        """
        Get actual generation output by BMU (Balancing Mechanism Unit).

        Args:
            settlement_date: Settlement date (YYYY-MM-DD)
            settlement_period: Settlement period (1-50), optional

        Returns:
            GenerationResponse with actual generation output data
        """
        params = {"SettlementDate": self._format_date(settlement_date)}

        if settlement_period is not None:
            self._validate_settlement_period(settlement_period)
            params["Period"] = settlement_period

        result = self._make_request("GET", "/PHYBMDATA", params=params)
        return GenerationResponse(**result)

    # ==================== Demand Data ====================

    def get_system_demand(
        self,
        from_date: Union[str, date],
        to_date: Union[str, date],
        settlement_period_from: Optional[int] = None,
        settlement_period_to: Optional[int] = None,
    ) -> SystemDemandResponse:
        """
        Get national demand data with typed response.

        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            settlement_period_from: Start settlement period (1-50), optional
            settlement_period_to: End settlement period (1-50), optional

        Returns:
            SystemDemandResponse with validated demand data
            
        Example:
            >>> response = client.get_system_demand(
            ...     from_date="2024-01-01",
            ...     to_date="2024-01-02"
            ... )
            >>> # response is SystemDemandResponse - fully typed!
            >>> for item in response.data:
            ...     print(f"Period {item['settlementPeriod']}: {item['demand']} MW")
        """
        params = {
            "FromSettlementDate": self._format_date(from_date),
            "ToSettlementDate": self._format_date(to_date),
        }

        if settlement_period_from is not None:
            self._validate_settlement_period(settlement_period_from)
            params["FromSettlementPeriod"] = settlement_period_from

        if settlement_period_to is not None:
            self._validate_settlement_period(settlement_period_to)
            params["ToSettlementPeriod"] = settlement_period_to

        result = self._make_request("GET", "/B0620", params=params)
        return SystemDemandResponse(**result)

    def get_forecast_demand(
        self, from_date: Union[str, date], to_date: Union[str, date]
    ) -> SystemDemandResponse:
        """
        Get forecast demand data.

        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            SystemDemandResponse with forecast demand data
        """
        params = {
            "FromSettlementDate": self._format_date(from_date),
            "ToSettlementDate": self._format_date(to_date),
        }

        result = self._make_request("GET", "/FORDAYDEM", params=params)
        return SystemDemandResponse(**result)

    # ==================== System Frequency ====================

    def get_system_frequency(
        self, from_date: Union[str, date, datetime], to_date: Union[str, date, datetime]
    ) -> SystemFrequencyResponse:
        """
        Get system frequency data.

        Args:
            from_date: Start date/datetime
            to_date: End date/datetime

        Returns:
            SystemFrequencyResponse with system frequency data
        """
        params = {
            "FromDateTime": self._format_date(from_date),
            "ToDateTime": self._format_date(to_date),
        }

        result = self._make_request("GET", "/FREQ", params=params)
        return SystemFrequencyResponse(**result)

    # ==================== Pricing Data ====================

    def get_system_prices(
        self,
        settlement_date: Union[str, date],
        settlement_period: Optional[int] = None,
    ) -> SystemPricesResponse:
        """
        Get system buy and sell prices.

        Args:
            settlement_date: Settlement date (YYYY-MM-DD)
            settlement_period: Settlement period (1-50), optional

        Returns:
            SystemPricesResponse with system prices data
        """
        params = {"SettlementDate": self._format_date(settlement_date)}

        if settlement_period is not None:
            self._validate_settlement_period(settlement_period)
            params["Period"] = settlement_period

        result = self._make_request("GET", "/SYSPRICE", params=params)
        return SystemPricesResponse(**result)

    def get_imbalance_prices(
        self,
        from_date: Union[str, date],
        to_date: Union[str, date],
    ) -> ImbalancePricesResponse:
        """
        Get imbalance prices.

        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            ImbalancePricesResponse with imbalance pricing data
        """
        params = {
            "FromSettlementDate": self._format_date(from_date),
            "ToSettlementDate": self._format_date(to_date),
        }

        result = self._make_request("GET", "/IMBALPRICES", params=params)
        return ImbalancePricesResponse(**result)

    # ==================== Balancing Services ====================

    def get_balancing_services_volume(
        self, settlement_date: Union[str, date]
    ) -> APIResponse:
        """
        Get balancing services volume data.

        Args:
            settlement_date: Settlement date (YYYY-MM-DD)

        Returns:
            APIResponse with balancing services volume data
        """
        params = {"SettlementDate": self._format_date(settlement_date)}
        result = self._make_request("GET", "/DISBSAD", params=params)
        return APIResponse(**result)

    # ==================== Wind Generation ====================

    def get_wind_generation_forecast(
        self, from_date: Union[str, date], to_date: Union[str, date]
    ) -> WindForecastResponse:
        """
        Get wind generation forecast.

        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            WindForecastResponse with wind generation forecast data
        """
        params = {
            "FromSettlementDate": self._format_date(from_date),
            "ToSettlementDate": self._format_date(to_date),
        }

        result = self._make_request("GET", "/WINDFOR", params=params)
        return WindForecastResponse(**result)

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self) -> "BMRSClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()

