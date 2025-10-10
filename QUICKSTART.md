# Quick Start Guide

Get started with the Elexon BMRS Python client in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/benjaminwatts/elexon-bmrs.git
cd elexon-bmrs

# Install the package
pip install -e .
```

## Get Your API Key

1. Visit [Elexon Portal](https://www.elexonportal.co.uk/)
2. Register for a free account
3. Generate an API key from your dashboard
4. Copy your API key for use in the examples below

## Your First Request

```python
from elexon_bmrs import BMRSClient
from datetime import date

# Initialize the client
client = BMRSClient(api_key="your-api-key-here")

# Get today's system demand
today = date.today()
demand = client.get_system_demand(
    from_date=today,
    to_date=today
)

print(demand)
```

## Common Use Cases

### 1. Get Generation Data

```python
from elexon_bmrs import BMRSClient
from datetime import date, timedelta

client = BMRSClient(api_key="your-api-key-here")

# Get generation by fuel type for the last 7 days
today = date.today()
week_ago = today - timedelta(days=7)

generation = client.get_generation_by_fuel_type(
    from_date=week_ago,
    to_date=today
)

print(f"Generation data: {generation}")
```

### 2. Get Current Prices

```python
from elexon_bmrs import BMRSClient
from datetime import date

client = BMRSClient(api_key="your-api-key-here")

# Get today's system prices
prices = client.get_system_prices(
    settlement_date=date.today()
)

print(f"Today's prices: {prices}")
```

### 3. Get Wind Forecast

```python
from elexon_bmrs import BMRSClient
from datetime import date, timedelta

client = BMRSClient(api_key="your-api-key-here")

# Get wind forecast for next 3 days
today = date.today()
three_days_later = today + timedelta(days=3)

wind_forecast = client.get_wind_generation_forecast(
    from_date=today,
    to_date=three_days_later
)

print(f"Wind forecast: {wind_forecast}")
```

## Using Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your API key
```

Then in your code:

```python
import os
from elexon_bmrs import BMRSClient

# Load from environment variable
api_key = os.getenv("BMRS_API_KEY")
client = BMRSClient(api_key=api_key)
```

## Error Handling

Always handle potential errors:

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import APIError, AuthenticationError

try:
    client = BMRSClient(api_key="your-api-key")
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
except AuthenticationError:
    print("Invalid API key!")
except APIError as e:
    print(f"API error: {e}")
```

## Next Steps

- Check out the [README.md](README.md) for complete documentation
- Explore [examples/basic_usage.py](examples/basic_usage.py) for more examples
- Read [examples/advanced_usage.py](examples/advanced_usage.py) for advanced patterns

## Available Methods

| Method | Description |
|--------|-------------|
| `get_generation_by_fuel_type()` | Generation data by fuel type |
| `get_actual_generation_output()` | Actual generation by BMU |
| `get_system_demand()` | National electricity demand |
| `get_forecast_demand()` | Demand forecast |
| `get_system_frequency()` | System frequency data |
| `get_system_prices()` | System buy/sell prices |
| `get_imbalance_prices()` | Imbalance pricing |
| `get_balancing_services_volume()` | Balancing services volume |
| `get_wind_generation_forecast()` | Wind generation forecast |
| `get_market_index()` | Market index data |

## Need Help?

- 📖 Read the full [documentation](README.md)
- 🐛 Report issues on [GitHub](https://github.com/benjaminwatts/elexon-bmrs/issues)
- 💡 Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Settlement Periods Explained

The UK electricity market uses 48 half-hour settlement periods per day:

- Period 1: 00:00-00:30
- Period 2: 00:30-01:00
- ...
- Period 48: 23:30-00:00

Some methods accept `settlement_period` as a parameter (1-50, with 49-50 for clock changes).

Happy coding! ⚡

