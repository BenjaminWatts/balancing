"""
Advanced usage examples for the Elexon BMRS Python client.

This script demonstrates error handling, custom configurations,
and more advanced data retrieval patterns.
"""

import logging
from datetime import date, timedelta
from typing import Dict, List, Any

from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual API key (get one at https://www.elexonportal.co.uk/)
# API key is optional but strongly recommended for higher rate limits
API_KEY = "your-api-key-here"


def example_error_handling():
    """Example: Comprehensive error handling."""
    print("=" * 60)
    print("Example 1: Error Handling")
    print("=" * 60)

    # Example 1: Authentication Error
    try:
        client = BMRSClient(api_key="invalid-key")
        client.get_system_demand(from_date=date.today(), to_date=date.today())
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e}")

    # Example 2: Validation Error
    try:
        client = BMRSClient(api_key=API_KEY)
        # Invalid settlement period (must be 1-50)
        client.get_market_index(settlement_date=date.today(), settlement_period=100)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")

    # Example 3: Rate Limit Error
    try:
        client = BMRSClient(api_key=API_KEY)
        # Make many requests in quick succession
        for i in range(100):
            client.get_system_demand(from_date=date.today(), to_date=date.today())
    except RateLimitError as e:
        logger.error(f"Rate limit exceeded. Retry after {e.retry_after} seconds")

    # Example 4: Generic API Error
    try:
        client = BMRSClient(api_key=API_KEY)
        client.get_system_demand(from_date=date.today(), to_date=date.today())
    except APIError as e:
        logger.error(f"API error: {e.status_code} - {e}")


def example_custom_configuration():
    """Example: Custom client configuration."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Configuration")
    print("=" * 60)

    # Create client with custom settings
    client = BMRSClient(
        api_key=API_KEY,
        base_url="https://api.bmreports.com/BMRS",  # Custom base URL
        timeout=60,  # Longer timeout
        verify_ssl=True,  # SSL verification
    )

    try:
        today = date.today()
        data = client.get_system_demand(from_date=today, to_date=today)
        logger.info(f"Retrieved data with custom configuration")
    finally:
        client.close()


def example_batch_data_retrieval():
    """Example: Retrieve multiple datasets in batch."""
    print("\n" + "=" * 60)
    print("Example 3: Batch Data Retrieval")
    print("=" * 60)

    results: Dict[str, Any] = {}

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()
        yesterday = today - timedelta(days=1)

        # Retrieve multiple datasets
        try:
            logger.info("Fetching generation data...")
            results["generation"] = client.get_generation_by_fuel_type(
                from_date=yesterday, to_date=today
            )

            logger.info("Fetching demand data...")
            results["demand"] = client.get_system_demand(
                from_date=yesterday, to_date=today
            )

            logger.info("Fetching pricing data...")
            results["prices"] = client.get_system_prices(settlement_date=today)

            logger.info("Fetching wind forecast...")
            results["wind_forecast"] = client.get_wind_generation_forecast(
                from_date=today, to_date=today + timedelta(days=2)
            )

            logger.info(f"Successfully retrieved {len(results)} datasets")

        except APIError as e:
            logger.error(f"Error retrieving data: {e}")

    return results


def example_date_range_iteration():
    """Example: Iterate over a date range to collect historical data."""
    print("\n" + "=" * 60)
    print("Example 4: Date Range Iteration")
    print("=" * 60)

    start_date = date.today() - timedelta(days=7)
    end_date = date.today()

    all_demand_data: List[Dict[str, Any]] = []

    with BMRSClient(api_key=API_KEY) as client:
        current_date = start_date

        while current_date <= end_date:
            try:
                logger.info(f"Fetching demand data for {current_date}")

                demand = client.get_system_demand(
                    from_date=current_date, to_date=current_date
                )

                all_demand_data.append(
                    {"date": current_date.isoformat(), "data": demand}
                )

            except APIError as e:
                logger.error(f"Error fetching data for {current_date}: {e}")

            current_date += timedelta(days=1)

    logger.info(f"Collected data for {len(all_demand_data)} days")
    return all_demand_data


def example_retry_logic():
    """Example: Implement retry logic for failed requests."""
    print("\n" + "=" * 60)
    print("Example 5: Retry Logic with Rate Limit Handling")
    print("=" * 60)

    import time

    max_retries = 3
    retry_delay = 2  # seconds

    with BMRSClient(api_key=API_KEY) as client:
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} of {max_retries}")

                data = client.get_system_demand(
                    from_date=date.today(), to_date=date.today()
                )

                logger.info("Request successful")
                return data

            except RateLimitError as e:
                if attempt == max_retries - 1:
                    logger.error("Max retries reached due to rate limiting")
                    raise
                
                # Respect the API's Retry-After header if provided
                if e.retry_after:
                    wait_time = e.retry_after
                    logger.warning(
                        f"Rate limited. API suggests waiting {wait_time} seconds..."
                    )
                else:
                    # Otherwise use exponential backoff
                    wait_time = retry_delay * (2**attempt)
                    logger.warning(
                        f"Rate limited. Implementing exponential backoff: {wait_time}s"
                    )
                
                time.sleep(wait_time)

            except APIError as e:
                if attempt == max_retries - 1:
                    logger.error(f"Max retries reached. Last error: {e}")
                    raise
                else:
                    logger.warning(f"Request failed: {e}. Retrying...")
                    time.sleep(retry_delay)


def example_production_rate_limiting():
    """Example: Production-ready rate limit handling wrapper."""
    print("\n" + "=" * 60)
    print("Example 7: Production Rate Limiting Wrapper")
    print("=" * 60)

    import time

    class RateLimitedClient:
        """Wrapper that adds automatic rate limit handling to any BMRSClient method."""
        
        def __init__(self, api_key: str, max_retries: int = 3, base_delay: float = 1.0):
            self.client = BMRSClient(api_key=api_key)
            self.max_retries = max_retries
            self.base_delay = base_delay
            self._request_count = 0
            self._last_request_time = None
        
        def request_with_backoff(self, method, *args, **kwargs):
            """
            Execute any client method with automatic rate limit handling.
            
            Args:
                method: The BMRSClient method to call
                *args, **kwargs: Arguments to pass to the method
            
            Returns:
                The result from the API call
            
            Raises:
                RateLimitError: If max retries exceeded
                APIError: If API returns an error
            """
            for attempt in range(self.max_retries):
                try:
                    # Track request metrics
                    self._request_count += 1
                    self._last_request_time = time.time()
                    
                    result = method(*args, **kwargs)
                    
                    if attempt > 0:
                        logger.info(f"Request succeeded after {attempt} retries")
                    
                    return result
                
                except RateLimitError as e:
                    if attempt == self.max_retries - 1:
                        logger.error(
                            f"Max retries ({self.max_retries}) exceeded for rate limiting"
                        )
                        raise
                    
                    # Calculate wait time
                    if e.retry_after:
                        wait_time = e.retry_after
                        logger.warning(
                            f"Rate limited. API suggests {wait_time}s wait "
                            f"(attempt {attempt + 1}/{self.max_retries})"
                        )
                    else:
                        wait_time = self.base_delay * (2 ** attempt)
                        logger.warning(
                            f"Rate limited. Exponential backoff: {wait_time}s "
                            f"(attempt {attempt + 1}/{self.max_retries})"
                        )
                    
                    time.sleep(wait_time)
                
                except APIError as e:
                    logger.error(f"API error on attempt {attempt + 1}: {e}")
                    if attempt == self.max_retries - 1:
                        raise
                    time.sleep(self.base_delay)
        
        def get_request_stats(self) -> Dict[str, Any]:
            """Get statistics about API usage."""
            return {
                "total_requests": self._request_count,
                "last_request_time": self._last_request_time,
            }
        
        def close(self):
            """Close the underlying client."""
            self.client.close()

    # Usage example
    rate_limited = RateLimitedClient(
        api_key=API_KEY,
        max_retries=5,
        base_delay=1.0
    )
    
    try:
        logger.info("Fetching data with automatic rate limit handling...")
        
        # Make multiple requests that might trigger rate limits
        today = date.today()
        
        demand = rate_limited.request_with_backoff(
            rate_limited.client.get_system_demand,
            from_date=today,
            to_date=today
        )
        logger.info(f"Demand data retrieved: {len(demand.get('data', []))} records")
        
        prices = rate_limited.request_with_backoff(
            rate_limited.client.get_system_prices,
            settlement_date=today
        )
        logger.info(f"Price data retrieved")
        
        # Show usage stats
        stats = rate_limited.get_request_stats()
        logger.info(f"Total requests made: {stats['total_requests']}")
        
    finally:
        rate_limited.close()
    
    logger.info("Rate-limited client wrapper example complete")


def example_data_comparison():
    """Example: Compare forecast vs actual data."""
    print("\n" + "=" * 60)
    print("Example 6: Forecast vs Actual Comparison")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()

        try:
            # Get forecast demand
            logger.info("Fetching forecast demand...")
            forecast = client.get_forecast_demand(from_date=today, to_date=today)

            # Get actual demand
            logger.info("Fetching actual demand...")
            actual = client.get_system_demand(from_date=today, to_date=today)

            # Compare the two
            logger.info("Forecast data retrieved:")
            logger.info(f"  Records: {len(forecast.get('data', []))}")

            logger.info("Actual data retrieved:")
            logger.info(f"  Records: {len(actual.get('data', []))}")

            return {"forecast": forecast, "actual": actual}

        except APIError as e:
            logger.error(f"Error comparing data: {e}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 8 + "Advanced Elexon BMRS Client Examples" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\nNote: Replace API_KEY with your actual API key to run these examples.\n")

    # Run all examples
    try:
        example_error_handling()
        example_custom_configuration()
        example_batch_data_retrieval()
        example_date_range_iteration()
        example_retry_logic()
        example_data_comparison()
        example_production_rate_limiting()

        print("\n" + "=" * 60)
        print("All advanced examples completed!")
        print("=" * 60 + "\n")

    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print("Make sure you have set a valid API key.")

