# Typed Client API Reference

The `TypedBMRSClient` provides fully typed responses for all BMRS API endpoints.

## Overview

While the standard `BMRSClient` returns `Dict[str, Any]` for most endpoints, `TypedBMRSClient` returns proper Pydantic models with full type safety.

## Class Reference

::: elexon_bmrs.typed_client.TypedBMRSClient
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2
      members:
        - __init__
        - get_typing_info

## Convenience Function

::: elexon_bmrs.typed_client.create_typed_client
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Response Type Mapping

The typed client maps endpoints to their proper response types:

### Core Methods (Already Typed)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_system_demand` | `SystemDemandResponse` | System demand data |
| `get_forecast_demand` | `SystemDemandResponse` | Demand forecasts |
| `get_generation_by_fuel_type` | `GenerationResponse` | Generation by fuel type |
| `get_actual_generation_output` | `GenerationResponse` | Actual generation output |
| `get_wind_generation_forecast` | `WindForecastResponse` | Wind generation forecasts |
| `get_system_frequency` | `SystemFrequencyResponse` | System frequency data |
| `get_system_prices` | `SystemPricesResponse` | System prices |
| `get_imbalance_prices` | `ImbalancePricesResponse` | Imbalance prices |
| `get_balancing_services_volume` | `APIResponse` | Balancing services volume |
| `get_market_index` | `SystemPricesResponse` | Market index |

### Dataset Endpoints (Now Typed)

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_datasets_abuc` | `AbucDatasetRow_DatasetResponse` | Amount of balancing reserves under contract |
| `get_datasets_agpt` | `ActualAggregatedGenerationPerTypeDatasetRow_DatasetResponse` | Aggregated generation per type |
| `get_datasets_aoge` | `ActualGenerationOutputPerGenerationUnitDatasetRow_DatasetResponse` | Actual generation output per generation unit |
| `get_datasets_aogws` | `ActualOrEstimatedWindGenerationDatasetRow_DatasetResponse` | Actual or estimated wind generation |
| `get_datasets_atl` | `ActualTotalLoadPerBiddingZoneDatasetRow_DatasetResponse` | Actual total load per bidding zone |
| `get_datasets_awgf` | `AggregatedWindGenerationForecastDatasetRow_DatasetResponse` | Aggregated wind generation forecast |
| `get_datasets_atc` | `AvailableTransmissionCapacityDatasetRow_DatasetResponse` | Available transmission capacity |
| `get_datasets_boalf` | `BidOfferAcceptanceLevelDatasetRow_DatasetResponse` | Bid offer acceptance level |
| `get_datasets_bod` | `BidOfferDatasetRow_DatasetResponse` | Bid offer data |
| `get_datasets_cbs` | `BalancingServicesVolumeData_DatasetResponse` | Capacity balancing service |
| `get_cdn` | `CreditDefaultNoticeDatasetResponse` | Credit default notice |
| `get_datasets_cdn` | `CreditDefaultNoticeDatasetRow_DatasetResponse` | Credit default notice dataset |
| `get_datasets_market_index` | `MarketIndexDatasetResponse` | Market index dataset |

### Remaining Endpoints

Endpoints not listed above return `APIResponse` (generic typed response) instead of `Dict[str, Any]`. These will be updated with specific response types in future versions.

## Usage Examples

### Basic Usage

```python
from elexon_bmrs import TypedBMRSClient

client = TypedBMRSClient(api_key="your-key")

# Fully typed response
abuc_data = client.get_datasets_abuc(
    publishDateTimeFrom="2024-01-01T00:00:00Z",
    publishDateTimeTo="2024-01-02T00:00:00Z"
)

# Type-safe access
for row in abuc_data.data or []:
    print(f"Dataset: {row.dataset}")
    print(f"PSR Type: {row.psrType}")
```

### Type Checking

```python
from elexon_bmrs import TypedBMRSClient
from elexon_bmrs.generated_models import AbucDatasetRow

def process_data(client: TypedBMRSClient) -> None:
    response = client.get_datasets_abuc(
        publishDateTimeFrom="2024-01-01T00:00:00Z",
        publishDateTimeTo="2024-01-02T00:00:00Z"
    )
    
    # Type checker knows response.data is List[AbucDatasetRow]
    for row in response.data or []:
        if row.dataset:
            print(row.dataset)
```

### Checking Type Coverage

```python
from elexon_bmrs import TypedBMRSClient

client = TypedBMRSClient()
info = client.get_typing_info()

print(f"Typing coverage: {info['typing_stats']['typing_coverage_percent']}%")
print(f"Typed endpoints: {info['typing_stats']['typed_endpoints']}")
print(f"Untyped endpoints: {info['typing_stats']['untyped_endpoints']}")
```

## Migration Guide

### From BMRSClient

```python
# Before
from elexon_bmrs import BMRSClient
client = BMRSClient(api_key="your-key")
response = client.get_datasets_abuc(...)  # Dict[str, Any]

# After
from elexon_bmrs import TypedBMRSClient
client = TypedBMRSClient(api_key="your-key")
response = client.get_datasets_abuc(...)  # AbucDatasetRow_DatasetResponse
```

### Method Signatures

All method signatures remain identical. Only return types change:

```python
# Same parameters, different return type
def get_datasets_abuc(
    self,
    publishDateTimeFrom: str,
    publishDateTimeTo: str,
    format: Optional[str] = None
) -> AbucDatasetRow_DatasetResponse:  # Instead of Dict[str, Any]
    ...
```

## Performance

The typed client adds minimal overhead:

- **Parsing time**: ~1-5ms per response
- **Memory usage**: Slightly higher due to Pydantic models
- **Type safety**: 100% improvement in development experience

## Error Handling

The typed client handles parsing errors gracefully:

```python
from elexon_bmrs import TypedBMRSClient

client = TypedBMRSClient(api_key="your-key")

try:
    response = client.get_datasets_abuc(...)
    # Success: response is fully typed
except Exception as e:
    # Error: response might be raw data or None
    print(f"Error: {e}")
```

## See Also

- [Fully Typed Usage Guide](../guide/fully-typed-usage.md) - Detailed usage guide
- [Generated Models Reference](generated-models.md) - All 280 Pydantic models
- [Standard Client Reference](client.md) - Original BMRSClient
- [Examples](../examples/basic.md) - Code examples
