# Type-Safe Usage

The library includes **280 auto-generated Pydantic models** for full type safety and IDE autocomplete support.

## Benefits of Type-Safe Usage

✅ **IDE Autocomplete** - Full IntelliSense/autocomplete support  
✅ **Type Checking** - Static type validation with mypy  
✅ **Data Validation** - Automatic validation with Pydantic  
✅ **Better Documentation** - Self-documenting code with type hints  
✅ **Fewer Bugs** - Catch errors at development time

## Specific Response Types

Each client method returns its own specific response type:

```python
from elexon_bmrs import (
    BMRSClient,
    SystemDemandResponse,      # for get_system_demand()
    GenerationResponse,         # for get_generation_by_fuel_type()
    WindForecastResponse,       # for get_wind_generation_forecast()
    SystemPricesResponse,       # for get_system_prices()
    SystemFrequencyResponse,    # for get_system_frequency()
    ImbalancePricesResponse,    # for get_imbalance_prices()
)

client = BMRSClient(api_key="your-key")

# Each method returns its specific type
demand: SystemDemandResponse = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

generation: GenerationResponse = client.get_generation_by_fuel_type(
    from_date="2024-01-01",
    to_date="2024-01-02"
)
```

## Using Generated Models

Import and use the auto-generated Pydantic models:

```python
from elexon_bmrs import BMRSClient, SystemDemandResponse
from elexon_bmrs.generated_models import DemandOutturnNational

client = BMRSClient(api_key="your-key")

# Get data with specific response type
response: SystemDemandResponse = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

# Parse with Pydantic model for full type safety
for item in response.data:
    demand = DemandOutturnNational(**item)
    
    # Full IDE autocomplete available!
    print(f"Date: {demand.settlement_date}")
    print(f"Period: {demand.settlement_period}")
    print(f"Demand: {demand.demand} MW")
    # Your IDE will show all available fields
```

## Common Generated Models

### Demand Models

```python
from elexon_bmrs.generated_models import (
    DemandOutturnNational,
    DemandOutturnTransmission,
)

# Parse demand data
for item in response.data:
    demand = DemandOutturnNational(**item)
    print(f"{demand.settlement_date}: {demand.demand} MW")
```

### Generation Models

```python
from elexon_bmrs.generated_models import (
    ActualAggregatedGenerationPerTypeDatasetRow,
    WindGenerationForecast,
)

# Parse generation data
for item in generation_response.data:
    gen = ActualAggregatedGenerationPerTypeDatasetRow(**item)
    print(f"Fuel Type: {gen.fuel_type}, Output: {gen.quantity} MW")
```

### Pricing Models

```python
from elexon_bmrs.generated_models import (
    SystemPrices,
    ImbalancePrices,
)

# Parse pricing data
for item in price_response.data:
    price = SystemPrices(**item)
    print(f"Period {price.settlement_period}: £{price.price}/MWh")
```

## Type Checking with mypy

Enable static type checking:

```python
from elexon_bmrs import BMRSClient, SystemDemandResponse
from elexon_bmrs.generated_models import DemandOutturnNational

def get_peak_demand(client: BMRSClient, date: str) -> float:
    """Get peak demand for a given date."""
    response: SystemDemandResponse = client.get_system_demand(
        from_date=date,
        to_date=date
    )
    
    demands = [DemandOutturnNational(**item) for item in response.data]
    return max(d.demand for d in demands)
```

Run mypy to check types:

```bash
mypy your_script.py
```

## Validation

Pydantic automatically validates data:

```python
from elexon_bmrs.generated_models import DemandOutturnNational
from pydantic import ValidationError

try:
    # Invalid data will raise ValidationError
    demand = DemandOutturnNational(
        settlement_date="invalid-date",
        settlement_period=999,  # Invalid period
        demand="not a number"   # Invalid type
    )
except ValidationError as e:
    print(f"Validation error: {e}")
    # Handle invalid data
```

## Custom Type Hints

Create your own type hints for domain logic:

```python
from typing import List
from elexon_bmrs.generated_models import DemandOutturnNational

DemandList = List[DemandOutturnNational]

def filter_peak_periods(demands: DemandList, threshold: float) -> DemandList:
    """Filter demand records above threshold."""
    return [d for d in demands if d.demand > threshold]

def calculate_average(demands: DemandList) -> float:
    """Calculate average demand."""
    return sum(d.demand for d in demands) / len(demands)
```

## IDE Support

### VS Code

Install Python extension for full IntelliSense:

```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true
}
```

### PyCharm

PyCharm automatically provides autocomplete for type-hinted code.

## Example: Full Type-Safe Workflow

```python
from datetime import date
from typing import Dict, List
from elexon_bmrs import BMRSClient, SystemDemandResponse
from elexon_bmrs.generated_models import DemandOutturnNational

def analyze_demand(api_key: str, target_date: str) -> Dict[str, float]:
    """
    Analyze demand data with full type safety.
    
    Args:
        api_key: BMRS API key
        target_date: Date to analyze (YYYY-MM-DD)
    
    Returns:
        Dictionary with demand statistics
    """
    client = BMRSClient(api_key=api_key)
    
    # Type-safe API call
    response: SystemDemandResponse = client.get_system_demand(
        from_date=target_date,
        to_date=target_date
    )
    
    # Type-safe parsing
    demands: List[DemandOutturnNational] = [
        DemandOutturnNational(**item)
        for item in response.data
    ]
    
    # Type-safe analysis
    demand_values = [d.demand for d in demands]
    
    return {
        "min": min(demand_values),
        "max": max(demand_values),
        "avg": sum(demand_values) / len(demand_values),
        "count": len(demand_values)
    }

# Usage with type hints
stats: Dict[str, float] = analyze_demand("your-key", "2024-01-01")
print(f"Peak demand: {stats['max']} MW")
```

## Next Steps

- [Error Handling](error-handling.md) - Handle errors with type safety
- [API Reference - Models](../api/models.md) - View all model documentation
- [API Reference - Generated Models](../api/generated-models.md) - View all 280 generated models
- [Examples](../examples/basic.md) - More usage examples

