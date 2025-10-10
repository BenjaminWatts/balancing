# Quick Start Guide

This guide will get you up and running with the Elexon BMRS Python client in minutes.

## Basic Example

```python
from elexon_bmrs import BMRSClient

# Initialize the client
client = BMRSClient(api_key="your-api-key-here")

# Get system demand data
demand = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

print(demand)
```

## Using Without an API Key

While not recommended, you can use the API without a key (with lower rate limits):

```python
from elexon_bmrs import BMRSClient

# Initialize without API key (warning will be logged)
client = BMRSClient()

demand = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)
```

!!! warning "API Key Recommended"
    While the API works without a key, Elexon strongly recommends using one for:
    
    - Higher rate limits
    - Better performance
    - Usage tracking and support
    
    Get your free API key at [Elexon Portal](https://www.elexonportal.co.uk/)

## Common Use Cases

### Getting Generation Data

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(api_key="your-api-key")

# Get generation by fuel type
generation = client.get_generation_by_fuel_type(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

print(f"Total records: {generation.get('totalRecords', 0)}")
for item in generation.get('data', []):
    print(f"{item['settlementDate']} Period {item['settlementPeriod']}")
    print(f"  Wind: {item.get('wind', 0)} MW")
    print(f"  Nuclear: {item.get('nuclear', 0)} MW")
    print(f"  CCGT: {item.get('ccgt', 0)} MW")
```

### Getting Pricing Data

```python
# Get system prices
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

### Getting Wind Forecast

```python
# Get wind generation forecast
wind_forecast = client.get_wind_generation_forecast(
    from_date="2024-01-01",
    to_date="2024-01-07"
)
```

## Type-Safe Usage

For better IDE support and type safety, use the typed response models:

```python
from elexon_bmrs import BMRSClient, SystemDemandResponse
from elexon_bmrs.generated_models import DemandOutturnNational

client = BMRSClient(api_key="your-api-key")

# Returns SystemDemandResponse automatically
response: SystemDemandResponse = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

# Full type safety with Pydantic models
for item in response.data:
    demand = DemandOutturnNational(**item)
    print(f"Date: {demand.settlement_date}")
    print(f"Demand: {demand.demand} MW")
    # Full IDE autocomplete available!
```

## Using Context Manager

For automatic cleanup of resources:

```python
from elexon_bmrs import BMRSClient

# Use as context manager
with BMRSClient(api_key="your-api-key") as client:
    demand = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
    print(demand)
# Session automatically closed
```

## Error Handling

Handle API errors gracefully:

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)

try:
    client = BMRSClient(api_key="your-api-key")
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Invalid input: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Settlement Periods

The UK electricity market operates in half-hour settlement periods:

- Each day has **48 settlement periods** (50 on clock change days)
- Period 1: 00:00-00:30
- Period 2: 00:30-01:00
- Period 48: 23:30-00:00

```python
# Get data for a specific settlement period
prices = client.get_system_prices(
    settlement_date="2024-01-01",
    settlement_period=10  # 04:30-05:00
)
```

## Next Steps

- [Authentication Guide](authentication.md) - Set up your API key
- [User Guide - Basic Usage](../guide/basic-usage.md) - More detailed examples
- [User Guide - Type-Safe Usage](../guide/typed-usage.md) - Advanced type safety
- [Error Handling Guide](../guide/error-handling.md) - Comprehensive error handling
- [API Reference](../api/client.md) - Complete method documentation

