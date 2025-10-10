# Generated Models Reference

This library includes **280 auto-generated Pydantic models** from the official BMRS OpenAPI specification. These models provide full type safety and IDE autocomplete for all API responses.

## Usage

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.generated_models import (
    DemandOutturnNational,
    ActualAggregatedGenerationPerTypeDatasetRow,
    WindGenerationForecast,
    # ... and 277 more!
)

client = BMRSClient(api_key="your-key")

# Get data from API
response = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

# Parse with Pydantic for full type safety
for item in response.data:
    demand = DemandOutturnNational(**item)
    # Full IDE autocomplete available!
    print(f"{demand.settlement_date}: {demand.demand} MW")
```

## Available Models

All generated models are available in the `elexon_bmrs.generated_models` module:

::: elexon_bmrs.generated_models
    options:
      show_root_heading: true
      show_source: false
      heading_level: 2
      group_by_category: true
      show_category_heading: true

## Model Generation

These models are automatically generated from the OpenAPI specification using our code generation tools. This ensures:

- ✅ **100% API coverage** - All endpoints and models included
- ✅ **Always up-to-date** - Can regenerate when API changes
- ✅ **Type safety** - Full Pydantic validation
- ✅ **IDE support** - Complete autocomplete

### Regenerating Models

If you're developing the library, you can regenerate models:

```bash
# Download latest OpenAPI spec
make download-schema

# Generate models
make generate-models

# Or do both
make generate-all
```

See the [Code Generation guide](../development/code-generation.md) for more details.

## Common Models

### Demand Models

- `DemandOutturnNational` - National demand outturn
- `DemandOutturnTransmission` - Transmission demand
- `DemandForecast` - Demand forecasts

### Generation Models

- `ActualAggregatedGenerationPerTypeDatasetRow` - Generation by fuel type
- `WindGenerationForecast` - Wind generation forecasts
- `ActualGenerationOutputPerGenerationUnit` - Generation by BMU

### Pricing Models

- `SystemPrices` - System buy/sell prices
- `ImbalancePrices` - Imbalance pricing data
- `MarketIndexData` - Market index prices

### System Models

- `SystemFrequency` - System frequency data
- `SystemWarnings` - System warnings and alerts
- `BalancingServicesVolume` - Balancing services data

## Type Safety Benefits

Using generated models provides several advantages:

### 1. Validation

```python
from elexon_bmrs.generated_models import DemandOutturnNational
from pydantic import ValidationError

try:
    demand = DemandOutturnNational(**data)
except ValidationError as e:
    print(f"Invalid data: {e}")
```

### 2. IDE Autocomplete

Your IDE will show all available fields and their types:

```python
demand = DemandOutturnNational(**data)
# IDE shows: settlement_date, settlement_period, demand, etc.
print(demand.demand)  # ✓ Autocomplete works!
```

### 3. Type Checking

Static type checkers like mypy can verify your code:

```python
def process_demand(demand: DemandOutturnNational) -> float:
    return demand.demand * 1.1  # Type-checked!
```

### 4. Documentation

Models include docstrings and field descriptions from the OpenAPI spec:

```python
from elexon_bmrs.generated_models import DemandOutturnNational

# View model documentation
help(DemandOutturnNational)
```

## Examples

See the [Typed Usage guide](../guide/typed-usage.md) and [Examples](../examples/basic.md) for comprehensive examples using generated models.

