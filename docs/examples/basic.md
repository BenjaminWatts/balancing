# Basic Examples

Complete working examples for common use cases.

## Example 1: Simple Demand Query

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(api_key="your-api-key")

demand = client.get_system_demand(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

print(f"Retrieved {len(demand['data'])} records")
```

## Example 2: Generation by Fuel Type

```python
generation = client.get_generation_by_fuel_type(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

for item in generation['data']:
    print(f"Wind: {item.get('wind', 0)} MW")
    print(f"Nuclear: {item.get('nuclear', 0)} MW")
```

## More Examples

For complete runnable examples, see:

- [examples/basic_usage.py](https://github.com/benjaminwatts/balancing/blob/main/examples/basic_usage.py)
- [examples/typed_usage.py](https://github.com/benjaminwatts/balancing/blob/main/examples/typed_usage.py)
