# Elexon BMRS Python Client

A Python client library for accessing the Elexon BMRS (Balancing Mechanism Reporting Service) API. This library provides easy access to UK electricity market data including generation, demand, pricing, and system information.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/elexon-bmrs.svg)](https://pypi.org/project/elexon-bmrs/)

## Features

- 🎯 **99% Type Coverage** - 284/287 endpoints return fully typed Pydantic models
- 🔌 **287 API Endpoints** - Complete coverage of all BMRS data
- 🔑 **API key optional** (but recommended for higher rate limits)
- 📊 **280+ Pydantic Models** - Auto-generated with comprehensive validation
- 🧩 **39 Field Mixins** - Massive code deduplication (~364+ lines saved)
- ⚡ **Full IDE Autocomplete** - Type-safe access to all response fields
- 🛡️ **Built-in error handling** - Pydantic validation with clear error messages
- 📝 **Complete Type Hints** - Works with mypy, pyright, and IDE type checking
- 🤖 **Auto-generated** - Always up-to-date with OpenAPI specification
- 🧪 **Comprehensive tests** - All endpoint categories tested
- ⚠️ **Clear Warnings** - 3 untyped endpoints clearly flagged (2 XML, 1 deprecated)
- 📚 **Complete documentation** - Examples and detailed docs for all endpoints

## Quick Start

```python
from elexon_bmrs import BMRSClient

# Initialize the client with your API key
client = BMRSClient(api_key="your-api-key-here")

# Get system demand data
demand = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

# Access any of the 287 available endpoints
dynamic_data = client.get_balancing_dynamic(
    bmUnit="2__HFLEX001",
    snapshotAt="2024-01-01T12:00:00Z"
)

print(demand)
```

## Endpoint Categories

The client provides **287 methods** organized into these categories:

- **Balancing Mechanism** (20+ endpoints) - Dynamic, physical, bid/offer, acceptances
- **Generation** (15+ endpoints) - By fuel type, BMU, wind/solar forecasts
- **Demand** (10+ endpoints) - National, transmission, peak, rolling demand
- **Pricing & Settlement** (25+ endpoints) - System prices, cashflows, volumes
- **Non-BM Services** (10+ endpoints) - STOR, DISBSAD, NETBSAD
- **System Data** (10+ endpoints) - Frequency, warnings, margin forecasts
- **Datasets** (150+ endpoints) - Direct access to 100+ BMRS datasets
- **Reference Data** (10+ endpoints) - BMUs, interconnectors, fuel types
- **Streaming** (40+ endpoints) - Real-time data streams

See the [Complete Endpoint Reference](api/all-endpoints.md) for the full list.

## Type-Safe Usage (v0.3.0+)

**99% of endpoints now return typed Pydantic models automatically!**

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.generated_models import (
    DynamicData_ResponseWithMetadata,
    AbucDatasetRow_DatasetResponse
)

client = BMRSClient(api_key="your-api-key")

# ✨ Fully typed responses - automatic Pydantic parsing!
result: DynamicData_ResponseWithMetadata = client.get_balancing_dynamic(
    bmUnit="2__CARR-1",
    snapshotAt="2024-01-01T12:00:00Z"
)

# Full IDE autocomplete on all fields! 🎉
for item in result.data:
    print(f"Dataset: {item.dataset}")
    print(f"Value: {item.value}")
    print(f"Time: {item.time}")
    # ↑ IDE shows all available fields - autocomplete everywhere!

# List responses are also fully typed
demand = client.get_demand_outturn_summary(
    from_="2024-01-01",
    to_="2024-01-02"
)
# Returns: List[RollingSystemDemand] - each item typed!

for d in demand:
    print(f"Demand: {d.demand} MW at {d.start_time}")
```

**Type Coverage:** 284/287 endpoints (99%) are fully typed with Pydantic models!

## Installation

Install from PyPI:

```bash
pip install elexon-bmrs
```

For development installation:

```bash
git clone https://github.com/benjaminwatts/balancing.git
cd balancing
pip install -e ".[dev]"
```

## Next Steps

- **[Installation Guide](getting-started/installation.md)** - Detailed installation instructions
- **[Quick Start Guide](getting-started/quickstart.md)** - Get up and running quickly
- **[API Reference](api/client.md)** - Complete API documentation
- **[Examples](examples/basic.md)** - Code examples and patterns

## Resources

- [Elexon BMRS Website](https://www.bmreports.com/)
- [Elexon Portal](https://www.elexonportal.co.uk/) - Register for API key
- [API Documentation](https://bmrs.elexon.co.uk/api-documentation/guidance)
- [GitHub Repository](https://github.com/benjaminwatts/balancing)
- [PyPI Package](https://pypi.org/project/elexon-bmrs/)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/benjaminwatts/balancing/blob/main/LICENSE) file for details.

## Disclaimer

This is an unofficial client library and is not affiliated with or endorsed by Elexon Limited. Use of the BMRS API is subject to Elexon's terms and conditions.

