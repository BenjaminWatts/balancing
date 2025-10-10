# Elexon BMRS Python Client

A Python client library for accessing the Elexon BMRS (Balancing Mechanism Reporting Service) API. This library provides easy access to UK electricity market data including generation, demand, pricing, and system information.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔌 **287 API endpoints** - Complete coverage of all BMRS data
- 🔑 **API key optional** (but recommended for higher rate limits)
- 📊 Access to comprehensive UK electricity market data
- 🔄 Support for multiple data streams (generation, demand, pricing, balancing, etc.)
- ⚡ **Specific response type for each endpoint** (SystemDemandResponse, GenerationResponse, etc.)
- 🛡️ Built-in error handling and validation
- 📝 Full type hints and IDE autocomplete
- 🤖 Auto-generated from OpenAPI specification (287 endpoints + 280 models - 100% coverage!)
- 🧪 Comprehensive test coverage
- 📚 **Complete documentation** with examples for all endpoints

## Installation

### From PyPI

```bash
pip install elexon-bmrs
```

### From Source

```bash
# Clone the repository
git clone https://github.com/benjaminwatts/elexon-bmrs.git
cd elexon-bmrs

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Verify Installation

```bash
python -c "from elexon_bmrs import BMRSClient; print('✓ Installation successful!')"
```

## API Key Setup

### Do I Need an API Key?

The API key is **optional but strongly recommended** by Elexon. While the API can function without a key, using one provides significant benefits:

✅ **Higher rate limits** - Avoid hitting rate limits during data retrieval  
✅ **Better performance** - Improved reliability and response times  
✅ **Usage tracking** - Monitor your API usage and get support  
✅ **Production ready** - Essential for any production application

### Getting Your API Key

1. Visit the [Elexon Portal](https://www.elexonportal.co.uk/)
2. Register for a free account
3. Navigate to the API section to generate your key
4. Copy your API key and keep it secure

⚠️ **Note:** If you initialize the client without an API key, you'll see a warning message. This is expected behavior.

## Quick Start

### Basic Usage (with API Key - Recommended)

```python
from elexon_bmrs import BMRSClient
from datetime import date

# Initialize the client with your API key (recommended)
client = BMRSClient(api_key="your-api-key-here")

# Get generation data by fuel type (returns Dict[str, Any])
generation_data = client.get_generation_by_fuel_type(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

print(generation_data)
```

### Using Without an API Key (Not Recommended)

```python
from elexon_bmrs import BMRSClient

# You can use the API without a key, but you'll see a warning
client = BMRSClient()  # ⚠️ Warning will be logged

# API calls work but with lower rate limits
demand_data = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)
```

### Type-Safe Usage (Recommended)

```python
from elexon_bmrs import BMRSClient, SystemDemandResponse
from elexon_bmrs.generated_models import DemandOutturnNational

# Initialize client
client = BMRSClient(api_key="your-api-key-here")

# Each method returns its own specific response type!
response: SystemDemandResponse = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)
# ↑ Returns SystemDemandResponse automatically - no manual parsing!

# response.data is already validated
for item in response.data:
    demand = DemandOutturnNational(**item)
    print(f"Date: {demand.settlement_date}, Demand: {demand.demand} MW")
    # ↑ Full IDE autocomplete for all fields!
```

### Context Manager

```python
from elexon_bmrs import BMRSClient

# Use as a context manager to ensure proper cleanup
with BMRSClient(api_key="your-api-key-here") as client:
    # Get system demand data
    demand = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
    print(demand)
```

## API Documentation

### Authentication

The API key is optional but **strongly recommended** by Elexon. 

#### With API Key (Recommended)
```python
client = BMRSClient(api_key="your-api-key-here")
```

#### Without API Key (Lower Rate Limits)
```python
# A warning will be logged recommending you use an API key
client = BMRSClient()
```

Get your free API key at: [Elexon Portal](https://www.elexonportal.co.uk/)

### Available Methods

The client provides **287 methods** for accessing BMRS data. All methods are auto-generated from the OpenAPI specification with full type hints and documentation.

#### Verify All Endpoints

```python
from elexon_bmrs import BMRSClient

client = BMRSClient()
methods = [m for m in dir(client) if m.startswith('get_')]
print(f"Total endpoints: {len(methods)}")  # 287

# Get help for any method
help(client.get_balancing_dynamic)
```

#### Complete Documentation

- **[All Endpoints](https://benjaminwatts.github.io/balancing/api/all-endpoints)** - Complete endpoint reference
- **[Method Reference](https://benjaminwatts.github.io/balancing/api/method-reference)** - Organized by category
- **[Client API](https://benjaminwatts.github.io/balancing/api/client)** - Auto-generated docs
- **[Full Documentation](https://benjaminwatts.github.io/balancing/)** - Complete documentation site

#### Quick Examples

##### Market Index Data

```python
# Get market index data
market_index = client.get_market_index(
    settlement_date="2024-01-01",
    settlement_period=10  # Optional: specific half-hour period (1-50)
)
```

#### Generation Data

```python
# Get generation by fuel type
generation = client.get_generation_by_fuel_type(
    from_date="2024-01-01",
    to_date="2024-01-02",
    settlement_period_from=1,  # Optional
    settlement_period_to=48     # Optional
)

# Get actual generation output by BMU
actual_generation = client.get_actual_generation_output(
    settlement_date="2024-01-01",
    settlement_period=10
)

# Get wind generation forecast
wind_forecast = client.get_wind_generation_forecast(
    from_date="2024-01-01",
    to_date="2024-01-07"
)
```

#### Demand Data

```python
# Get system demand
demand = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

# Get forecast demand
forecast = client.get_forecast_demand(
    from_date="2024-01-01",
    to_date="2024-01-07"
)
```

#### System Frequency

```python
# Get system frequency data
frequency = client.get_system_frequency(
    from_date="2024-01-01",
    to_date="2024-01-02"
)
```

#### Pricing Data

```python
# Get system prices (buy and sell)
prices = client.get_system_prices(
    settlement_date="2024-01-01",
    settlement_period=10
)

# Get imbalance prices
imbalance = client.get_imbalance_prices(
    from_date="2024-01-01",
    to_date="2024-01-02"
)
```

#### Balancing Services

```python
# Get balancing services volume
balancing = client.get_balancing_services_volume(
    settlement_date="2024-01-01"
)
```

## Settlement Periods

The UK electricity market operates in half-hour settlement periods:
- Each day has 48 settlement periods (or 50 on clock change days)
- Period 1: 00:00-00:30
- Period 2: 00:30-01:00
- ...
- Period 48: 23:30-00:00

## Rate Limiting

The Elexon BMRS API implements rate limiting to ensure fair usage and system stability. While specific rate limits are not publicly documented, users are expected to use the API responsibly. Excessive requests may result in access restrictions or revocation of API keys.

### How Rate Limiting Works

When you exceed the rate limit, the API returns a `429 Too Many Requests` status code. The client automatically detects this and raises a `RateLimitError` with optional retry timing information.

### Handling Rate Limits

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import RateLimitError
import time

client = BMRSClient(api_key="your-api-key")

try:
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
except RateLimitError as e:
    # The exception includes retry_after in seconds (if provided by API)
    if e.retry_after:
        print(f"Rate limited. Waiting {e.retry_after} seconds...")
        time.sleep(e.retry_after)
    else:
        print("Rate limited. Implementing backoff...")
        time.sleep(60)  # Default wait time
```

### Retry Logic with Exponential Backoff

For production applications, implement exponential backoff to handle rate limits gracefully:

```python
import time
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import RateLimitError

def fetch_with_retry(client, max_retries=3):
    """Fetch data with exponential backoff on rate limits."""
    for attempt in range(max_retries):
        try:
            return client.get_system_demand(
                from_date="2024-01-01",
                to_date="2024-01-02"
            )
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise  # Re-raise on final attempt
            
            # Use API's retry_after or exponential backoff
            wait_time = e.retry_after if e.retry_after else (2 ** attempt)
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

client = BMRSClient(api_key="your-api-key")
data = fetch_with_retry(client)
```

### Best Practices to Avoid Rate Limits

1. **Implement Exponential Backoff**: Wait progressively longer between retries
2. **Cache Responses**: Store frequently accessed data locally to reduce API calls
3. **Batch Requests**: Use date ranges instead of individual requests when possible
4. **Use Streaming Endpoints**: For real-time data, use `/stream` endpoints instead of polling
5. **Monitor Your Usage**: Track API calls and implement throttling in your application
6. **Avoid Parallel Requests**: Sequential requests are more rate-limit friendly
7. **Use Appropriate Intervals**: Don't poll more frequently than your data actually updates

### Rate Limit Headers

When a rate limit is encountered, the API may return:
- `Retry-After`: Number of seconds to wait before retrying
- The client automatically extracts this value and includes it in `RateLimitError.retry_after`

### Example: Production-Ready Rate Limit Handling

```python
import time
import logging
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import RateLimitError, APIError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimitedClient:
    def __init__(self, api_key, max_retries=3, base_delay=1):
        self.client = BMRSClient(api_key=api_key)
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def request_with_backoff(self, func, *args, **kwargs):
        """Execute any client method with automatic retry on rate limits."""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError as e:
                if attempt == self.max_retries - 1:
                    logger.error("Max retries exceeded for rate limit")
                    raise
                
                # Use API's suggestion or exponential backoff
                if e.retry_after:
                    wait_time = e.retry_after
                else:
                    wait_time = self.base_delay * (2 ** attempt)
                
                logger.warning(f"Rate limited. Retry {attempt + 1}/{self.max_retries} "
                             f"after {wait_time}s")
                time.sleep(wait_time)
            except APIError as e:
                logger.error(f"API error: {e}")
                raise

# Usage
rate_limited_client = RateLimitedClient(api_key="your-api-key")
data = rate_limited_client.request_with_backoff(
    rate_limited_client.client.get_system_demand,
    from_date="2024-01-01",
    to_date="2024-01-02"
)
```

For more details on responsible API usage, see the [Elexon API Terms](https://www.elexon.co.uk/bsc/data/balancing-mechanism-reporting-agent/copyright-licence-use-bmrs-api/).

## Error Handling

The library provides specific exceptions for different error scenarios:

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)

try:
    client = BMRSClient(api_key="invalid-key")
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Invalid input: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/benjaminwatts/elexon-bmrs.git
cd elexon-bmrs

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Generation from OpenAPI Specification

This project includes tools to automatically generate and validate client code from the official BMRS API OpenAPI specification:

```bash
# Download the latest API specification
python tools/download_schema.py

# Generate client methods from the spec
python tools/generate_client.py

# Generate Pydantic models from the spec (142 models!)
python tools/generate_models.py

# Or generate everything at once
make generate-all

# Validate existing client against the spec
python tools/validate_client.py
```

**Benefits:**
- ✓ Automatically stay up-to-date with API changes
- ✓ Ensure complete coverage of all endpoints
- ✓ Type-safe responses with Pydantic models
- ✓ Maintain consistency with official API documentation
- ✓ Detect breaking changes early
- ✓ IDE autocomplete for all response fields

See [tools/README.md](tools/README.md) for detailed documentation on code generation.

### Using Generated Pydantic Models

The SDK includes **142 auto-generated Pydantic models** from the OpenAPI spec:

```python
# Import generated models
from elexon_bmrs.generated_models import (
    DemandOutturnNational,
    DemandOutturnTransmission,
    ActualAggregatedGenerationPerTypeDatasetRow,
    WindGenerationForecast,
    # ... and 138 more!
)

# Use with API responses for type safety
response = client.get_system_demand(from_date="2024-01-01", to_date="2024-01-02")

# Parse with Pydantic for validation and type safety
for item in response["data"]:
    demand = DemandOutturnNational(**item)
    # Now you have full IDE autocomplete and type checking!
    print(f"{demand.settlement_date}: {demand.demand} MW")
```

See [examples/typed_usage.py](examples/typed_usage.py) for comprehensive type-safe usage examples.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=elexon_bmrs --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

### Code Quality

```bash
# Format code with black
black elexon_bmrs tests

# Sort imports
isort elexon_bmrs tests

# Run linter
flake8 elexon_bmrs tests

# Type checking
mypy elexon_bmrs
```

## Examples

See the `examples/` directory for more detailed examples:

- `basic_usage.py` - Basic client usage examples
- `advanced_usage.py` - Advanced features and error handling
- `data_analysis.py` - Example data analysis workflows

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Workflow

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install dev dependencies (`pip install -e ".[dev]"`)
4. Make your changes
5. Run tests and checks (`make pre-release`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### For Maintainers: PyPI Distribution

**🚀 Automated (Recommended)**: Use GitHub Actions for automated publishing
- Quick [5-minute setup](GITHUB_ACTIONS_SETUP.md)
- Publishes automatically on GitHub Release
- Secure with trusted publishing (no API tokens!)
- Full CI/CD with testing

**🛠️ Manual**: Traditional command-line publishing
- Detailed [manual guide](PYPI_DISTRIBUTION.md)
- Use when you need direct control

```bash
# Automated (GitHub Actions) - Recommended
git tag v0.1.0 && git push origin v0.1.0
# Create GitHub Release → Automatic publish! 🎉

# Manual (Traditional)
make pre-release    # Run all checks
make upload-test    # Test on TestPyPI
make upload         # Publish to PyPI
```

## Resources

- [Elexon BMRS Website](https://www.bmreports.com/)
- [Elexon Portal](https://www.elexonportal.co.uk/) - Register for API key
- [API Documentation](https://bmrs.elexon.co.uk/api-documentation/guidance) - Official API docs
- [API Base URL](https://data.elexon.co.uk/bmrs/api/v1) - Production endpoint

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial client library and is not affiliated with or endorsed by Elexon Limited. Use of the BMRS API is subject to Elexon's terms and conditions.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes between versions.

### Version 0.1.0 (Upcoming)

- Initial release with core functionality
- 280 auto-generated Pydantic models (100% coverage)
- Support for generation, demand, pricing, and system data
- API key optional but recommended
- Comprehensive error handling
- Full type hints and IDE autocomplete
- Extensive documentation and examples

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/benjaminwatts/elexon-bmrs).

