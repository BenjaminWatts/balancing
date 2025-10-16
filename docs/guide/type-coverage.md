# Type Coverage Guide

## Overview

The `elexon-bmrs` SDK provides **99% type coverage** with comprehensive Pydantic models.

**284 out of 287 endpoints (98.9%)** return fully typed Pydantic models!

---

## 📊 Coverage Statistics

| Category | Count | Percentage | Details |
|----------|-------|------------|---------|
| **Fully Typed** | **284** | **98.9%** | ✅ Pydantic models |
| Single Model Returns | 181 | 63% | Auto-generated |
| List[Model] Returns | 91 | 32% | Auto-generated |
| List[str] Returns | 4 | 1.4% | Simple strings |
| Manual Models | 8 | 2.8% | Created from API |
| **Untyped** | **3** | **1.1%** | ⚠️ Cannot type |
| XML Endpoints | 2 | 0.7% | Return XML |
| Deprecated (404) | 1 | 0.3% | Doesn't exist |

---

## ✨ What This Means

### Typed Endpoints (284)

Get **full IDE autocomplete** and **type checking**:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(api_key="your-key")

# Returns: DynamicData_ResponseWithMetadata
result = client.get_balancing_dynamic(
    bmUnit="2__CARR-1",
    snapshotAt="2024-01-01T12:00:00Z"
)

# IDE knows result.data is List[DynamicData]
for item in result.data:
    # Autocomplete shows: dataset, bmUnit, value, time, etc.
    print(item.dataset, item.value)
```

### Untyped Endpoints (3)

Must handle manually:

```python
# Returns: Dict[str, Any] with warning
result = client.get_interop_message_list_retrieval(...)
# No autocomplete - manual structure handling required
```

---

## 🎯 Response Type Patterns

### 1. Single Model Response (181 endpoints)

Returns a wrapper object with `.data` array:

```python
result = client.get_balancing_dynamic(...)
# Type: DynamicData_ResponseWithMetadata

# Access data
for item in result.data:
    print(item.dataset, item.value)
```

### 2. List of Models (91 endpoints)

Returns a direct list of Pydantic models:

```python
demand = client.get_demand_outturn_summary(...)
# Type: List[RollingSystemDemand]

# Direct list iteration
for item in demand:
    print(item.demand, item.settlement_date)
```

### 3. List of Strings (4 endpoints)

Returns simple string arrays:

```python
fuels = client.get_reference_fueltypes_all()
# Type: List[str]
# Returns: ['CCGT', 'NUCLEAR', 'WIND', ...]

for fuel in fuels:
    print(fuel)
```

### 4. Manual Models (8 endpoints)

Created from actual API responses:

```python
health = client.get_health()
# Type: HealthCheckResponse

print(f"Status: {health.status}")
```

---

## 🧩 Field Mixins

**39 field mixins** eliminate code duplication across the 280 Pydantic models:

### Top 10 Most Used Mixins

| Mixin | Usage | Fields Provided |
|-------|-------|-----------------|
| `PublishTimeFields` | 86 models | `publish_time` |
| `DatasetFields` | 80 models | `dataset` |
| `SettlementFields` | 71 models | `settlement_date`, `settlement_period` |
| `StartTimeFields` | 54 models | `start_time` |
| `BmUnitFields` | 22 models | `bmu_id`, `national_grid_bm_unit` |
| `DocumentFields` | 19 models | `document_id`, `document_revision_number` |
| `DemandFields` | 13 models | `demand` |
| `PsrTypeFields` | 13 models | `psr_type` |
| `FuelTypeFields` | 12 models | `fuel_type` |
| `BoundaryFields` | 10 models | `boundary` |

**Result:** ~364+ lines of code saved through reuse!

---

## ⚠️ Untyped Endpoints

### Why Only 3 Remain Untyped

These 3 endpoints **cannot be typed** with Pydantic JSON models:

#### 1. XML Endpoints (2)
- `get_interop_message_list_retrieval()` - Returns XML
- `get_interop_message_detail_retrieval()` - Returns XML

**Reason:** Pydantic is for JSON validation, not XML. Would need XML schema support.

#### 2. Deprecated Endpoint (1)
- `get_lolpdrm_forecast_evolution()` - Returns 404

**Reason:** Endpoint doesn't exist in the API (removed/deprecated).

### Complete Details

See [UNTYPED_ENDPOINTS.md](https://github.com/BenjaminWatts/balancing/blob/main/UNTYPED_ENDPOINTS.md) for:
- Complete list with examples
- Best practices for handling them
- Typed alternatives where available

---

## 💡 Migration from v0.2.x

### No Breaking Changes!

Your existing code works without modification:

```python
# v0.2.x code still works in v0.3.0
result = client.get_datasets_abuc(...)
if 'data' in result:
    for item in result['data']:
        print(item['quantity'])
```

### Optional: Add Type Hints

Take advantage of the new typing:

```python
# v0.3.0 - Add type hints for better DX
from elexon_bmrs.generated_models import AbucDatasetRow_DatasetResponse

result: AbucDatasetRow_DatasetResponse = client.get_datasets_abuc(...)
for row in result.data:
    print(row.quantity)  # Full autocomplete!
```

---

## 🛠️ Type Checking

### With mypy

```bash
# Install mypy
pip install mypy

# Check your code
mypy your_script.py
```

### With pyright

```bash
# Install pyright
pip install pyright

# Check your code
pyright your_script.py
```

### In Your IDE

Modern IDEs (VSCode, PyCharm, etc.) automatically use type hints for:
- Autocomplete
- Error detection
- Inline documentation
- Refactoring support

---

## 📈 Benefits of Full Typing

### 1. IDE Autocomplete

```python
result = client.get_datasets_abuc(...)
result.  # IDE shows: data, metadata, total_records
result.data[0].  # IDE shows: dataset, publishTime, psrType, quantity, ...
```

### 2. Type Checking

```python
def process(data: AbucDatasetRow_DatasetResponse) -> float:
    # Type checker verifies data.data exists and is correct type
    return sum(row.quantity for row in data.data)
```

### 3. Validation

```python
# Pydantic automatically validates all fields
result = client.get_datasets_abuc(...)
# If API returns invalid data:
# - Clear validation error with field name
# - Falls back to raw data with warning
```

### 4. Documentation

```python
# Type hints serve as inline documentation
def analyze(
    client: BMRSClient,
    start: str
) -> DynamicData_ResponseWithMetadata:
    # Return type tells you exactly what to expect
    return client.get_balancing_dynamic(...)
```

---

## 🎯 Conclusion

**99% type coverage** represents **100% of all typeable JSON endpoints** in the BMRS API!

The remaining 1% (3 endpoints) physically cannot be typed:
- XML responses (2)
- Non-existent endpoint (1)

**This is the best-in-class Python SDK for the BMRS API!** 🏆

