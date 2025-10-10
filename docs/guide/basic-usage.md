# Basic Usage

This guide covers the fundamental usage patterns of the Elexon BMRS Python client.

## Initializing the Client

### With API Key (Recommended)

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(api_key="your-api-key-here")
```

### Without API Key

```python
from elexon_bmrs import BMRSClient

# Works but with lower rate limits
client = BMRSClient()
```

## Common Data Retrieval Patterns

### System Demand

Get electricity demand data:

```python
from datetime import date
from elexon_bmrs import BMRSClient

client = BMRSClient(api_key="your-key")

demand = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

print(f"Total records: {len(demand['data'])}")
for item in demand['data']:
    print(f"Period {item['settlementPeriod']}: {item['demand']} MW")
```

### Generation by Fuel Type

Get generation breakdown by fuel source:

```python
generation = client.get_generation_by_fuel_type(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

for item in generation['data']:
    print(f"{item['settlementDate']} Period {item['settlementPeriod']}")
    print(f"  Wind: {item.get('wind', 0)} MW")
    print(f"  Nuclear: {item.get('nuclear', 0)} MW")
    print(f"  CCGT: {item.get('ccgt', 0)} MW")
```

### System Prices

Get electricity market prices:

```python
# Get prices for specific settlement period
prices = client.get_system_prices(
    settlement_date="2024-01-01",
    settlement_period=10
)

# Get imbalance prices over date range
imbalance = client.get_imbalance_prices(
    from_date="2024-01-01",
    to_date="2024-01-02"
)
```

### Wind Generation Forecast

Get wind generation forecasts:

```python
from datetime import timedelta

today = date.today()
next_week = today + timedelta(days=7)

wind_forecast = client.get_wind_generation_forecast(
    from_date=today,
    to_date=next_week
)
```

### System Frequency

Get system frequency measurements:

```python
frequency = client.get_system_frequency(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

for item in frequency['data']:
    print(f"{item['timestamp']}: {item['frequency']} Hz")
```

## Response Structure

All endpoints return data in a standard format:

```python
{
    "data": [
        {
            "settlementDate": "2024-01-01",
            "settlementPeriod": 1,
            # ... additional fields
        }
    ],
    "metadata": {
        # Optional metadata
    },
    "totalRecords": 48
}
```

Access the data:

```python
response = client.get_system_demand(from_date="2024-01-01", to_date="2024-01-01")

# Get the data records
records = response['data']

# Get metadata if available
metadata = response.get('metadata', {})

# Get total record count
total = response.get('totalRecords', 0)
```

## Settlement Periods

The UK electricity market uses half-hour settlement periods:

- Each day has **48 settlement periods** (50 on clock change days)
- Period 1: 00:00-00:30
- Period 2: 00:30-01:00
- ...
- Period 48: 23:30-00:00

Filter by settlement period:

```python
# Get data for specific periods
demand = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-01",
    settlement_period_from=1,   # 00:00-00:30
    settlement_period_to=10      # 04:30-05:00
)
```

## Context Manager

Use the client as a context manager for automatic cleanup:

```python
with BMRSClient(api_key="your-key") as client:
    demand = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
    # Process data...
# Client automatically closed
```

## Manual Cleanup

If not using a context manager, remember to close the client:

```python
client = BMRSClient(api_key="your-key")

try:
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
finally:
    client.close()
```

## Date Handling

The client accepts dates in multiple formats:

```python
from datetime import date

# String format
client.get_system_demand(from_date="2024-01-01", to_date="2024-01-02")

# Date object
today = date.today()
client.get_system_demand(from_date=today, to_date=today)

# datetime object also works
from datetime import datetime
now = datetime.now()
client.get_system_demand(from_date=now.date(), to_date=now.date())
```

## Next Steps

- [Type-Safe Usage](typed-usage.md) - Use Pydantic models for type safety
- [Error Handling](error-handling.md) - Handle errors gracefully
- [Rate Limiting](rate-limiting.md) - Manage API rate limits
- [Examples](../examples/basic.md) - More code examples

