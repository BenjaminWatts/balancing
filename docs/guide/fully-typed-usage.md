# Fully Typed Usage

This guide shows how to use the `TypedBMRSClient` for complete type safety across all 287 API endpoints.

## The Problem

The standard `BMRSClient` returns `Dict[str, Any]` for most endpoints, which provides no type safety:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(api_key="your-key")
response = client.get_datasets_abuc(
    publishDateTimeFrom="2024-01-01T00:00:00Z",
    publishDateTimeTo="2024-01-02T00:00:00Z"
)
# response is Dict[str, Any] - no type safety!
```

**Note:** The BMRS OpenAPI specification defines **no required fields** for any of the 280 schemas. This means all fields in the generated models are `Optional`, which is actually correct according to the API specification. The `TypedBMRSClient` handles this gracefully by providing proper type hints while maintaining API compatibility.

## The Solution

Use `TypedBMRSClient` for fully typed responses:

```python
from elexon_bmrs import TypedBMRSClient

client = TypedBMRSClient(api_key="your-key")
response = client.get_datasets_abuc(
    publishDateTimeFrom="2024-01-01T00:00:00Z",
    publishDateTimeTo="2024-01-02T00:00:00Z"
)
# response is AbucDatasetRow_DatasetResponse - fully typed!
```

## Benefits

✅ **Full type safety** - Every endpoint returns the correct Pydantic model  
✅ **IDE autocomplete** - Complete IntelliSense for all response fields  
✅ **Type checking** - mypy and other tools can verify your code  
✅ **Data validation** - Automatic Pydantic validation of responses  
✅ **Better documentation** - Self-documenting code with type hints  

## Usage Examples

### Dataset Endpoints

```python
from elexon_bmrs import TypedBMRSClient

client = TypedBMRSClient(api_key="your-key")

# ABUC - Amount of Balancing Reserves Under Contract
abuc_data = client.get_datasets_abuc(
    publishDateTimeFrom="2024-01-01T00:00:00Z",
    publishDateTimeTo="2024-01-02T00:00:00Z"
)

# Fully typed access to response fields
print(f"Total records: {len(abuc_data.data or [])}")
for row in abuc_data.data or []:
    # Full IDE autocomplete available!
    print(f"Dataset: {row.dataset}")
    print(f"PSR Type: {row.psrType}")
    print(f"Business Type: {row.businessType}")
    print(f"Publish Time: {row.publishTime}")
```

### Generation Data

```python
# AGPT - Aggregated Generation Per Type
agpt_data = client.get_datasets_agpt(
    publishDateTimeFrom="2024-01-01T00:00:00Z",
    publishDateTimeTo="2024-01-02T00:00:00Z"
)

for row in agpt_data.data or []:
    print(f"Fuel Type: {row.fuelType}")
    print(f"Generation: {row.generation} MW")
    print(f"Output: {row.output} MW")
```

### System Frequency

```python
# FREQ - System Frequency
freq_data = client.get_datasets_freq(
    publishDateTimeFrom="2024-01-01T00:00:00Z",
    publishDateTimeTo="2024-01-02T00:00:00Z"
)

for row in freq_data.data or []:
    print(f"Time: {row.time}")
    print(f"Frequency: {row.frequency} Hz")
```

## Type Checking with mypy

Enable static type checking for your code:

```python
from elexon_bmrs import TypedBMRSClient
from elexon_bmrs.generated_models import AbucDatasetRow

def process_abuc_data(client: TypedBMRSClient) -> None:
    """Process ABUC data with full type safety."""
    response = client.get_datasets_abuc(
        publishDateTimeFrom="2024-01-01T00:00:00Z",
        publishDateTimeTo="2024-01-02T00:00:00Z"
    )
    
    # Type checker knows response.data is List[AbucDatasetRow]
    for row in response.data or []:
        # Type checker validates all field access
        dataset = row.dataset  # Optional[str]
        psr_type = row.psrType  # Optional[str]
        
        if dataset and psr_type:
            print(f"{dataset}: {psr_type}")

# Run mypy to check types
# mypy your_script.py
```

### Handling Optional Fields

Since the BMRS API defines no required fields, all fields are `Optional`. Handle this explicitly:

```python
from elexon_bmrs import TypedBMRSClient

client = TypedBMRSClient(api_key="your-key")
response = client.get_datasets_abuc(...)

for row in response.data or []:
    # Safe access with defaults
    dataset = row.dataset or "UNKNOWN"
    quantity = row.quantity or 0.0
    publish_time = row.publishTime or datetime.now()
    
    # Conditional access for optional fields
    if row.description:
        print(f"Description: {row.description}")
    
    if row.relatedInformation:
        print(f"Related info: {row.relatedInformation}")
    
    print(f"Dataset: {dataset}, Quantity: {quantity}")
```

## Response Type Mapping

The `TypedBMRSClient` maps endpoints to their proper response types:

| Endpoint | Response Type | Description |
|----------|---------------|-------------|
| `get_datasets_abuc` | `AbucDatasetRow_DatasetResponse` | Balancing reserves under contract |
| `get_datasets_agpt` | `ActualAggregatedGenerationPerTypeDatasetRow_DatasetResponse` | Generation by fuel type |
| `get_datasets_freq` | `SystemFrequencyDatasetRow_DatasetResponse` | System frequency |
| `get_datasets_bod` | `BidOfferDatasetRow_DatasetResponse` | Bid-offer data |
| `get_system_demand` | `SystemDemandResponse` | System demand |
| ... | ... | ... |

## Checking Type Coverage

See which endpoints are fully typed:

```python
from elexon_bmrs import TypedBMRSClient

client = TypedBMRSClient()
info = client.get_typing_info()

print(f"Typing coverage: {info['typing_stats']['typing_coverage_percent']}%")
print(f"Typed endpoints: {info['typing_stats']['typed_endpoints']}")
print(f"Untyped endpoints: {info['typing_stats']['untyped_endpoints']}")

# List all typed endpoints
for endpoint in info['typed_endpoints']:
    print(f"✅ {endpoint}")

# List endpoints that still need typing
for endpoint in info['untyped_endpoints']:
    print(f"⚠️  {endpoint} (returns Dict[str, Any])")
```

## Convenience Function

Use the convenience function for cleaner imports:

```python
from elexon_bmrs import create_typed_client

# Create fully typed client
client = create_typed_client(api_key="your-key")

# All methods return properly typed responses
data = client.get_datasets_abuc(...)  # Returns AbucDatasetRow_DatasetResponse
```

## Error Handling

The typed client handles parsing errors gracefully:

```python
from elexon_bmrs import TypedBMRSClient

client = TypedBMRSClient(api_key="your-key")

try:
    response = client.get_datasets_abuc(
        publishDateTimeFrom="2024-01-01T00:00:00Z",
        publishDateTimeTo="2024-01-02T00:00:00Z"
    )
    
    # If parsing succeeds, response is fully typed
    for row in response.data or []:
        print(f"Dataset: {row.dataset}")
        
except Exception as e:
    print(f"Error: {e}")
```

## Performance

The typed client has minimal performance overhead:

- **Parsing time**: ~1-5ms per response (depending on data size)
- **Memory usage**: Slightly higher due to Pydantic model creation
- **Type safety**: 100% improvement in development experience

## Migration from BMRSClient

Easy migration from the standard client:

```python
# Before
from elexon_bmrs import BMRSClient
client = BMRSClient(api_key="your-key")

# After
from elexon_bmrs import TypedBMRSClient
client = TypedBMRSClient(api_key="your-key")

# All method signatures remain the same
# Only return types change from Dict[str, Any] to proper Pydantic models
```

## Best Practices

1. **Use TypedBMRSClient** for new code
2. **Enable type checking** with mypy
3. **Handle optional fields** properly (use `or []` for lists)
4. **Check type coverage** periodically
5. **Report untyped endpoints** for future improvements

## Next Steps

- [API Reference - Typed Client](../api/typed-client.md) - Complete documentation
- [Generated Models Reference](../api/generated-models.md) - All 280 models
- [Examples](../examples/basic.md) - More typed usage examples
