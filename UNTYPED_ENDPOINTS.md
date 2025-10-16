# ⚠️ Untyped Endpoints Reference

## Overview

Out of 287 total endpoints, **12 endpoints (4%)** return `Dict[str, Any]` instead of typed Pydantic models.

**Why?** These endpoints either:
1. Have no response schema in the OpenAPI specification (11 endpoints)
2. Return streaming data (1 endpoint)

---

## ⚠️ What This Means for You

When using these endpoints:

- ❌ **No IDE autocomplete** on response fields
- ❌ **No type checking** with mypy/pyright
- ❌ **No Pydantic validation** of response data
- ❌ **No field documentation** in your IDE

You'll need to:
- ✅ Check the API documentation manually
- ✅ Handle responses carefully with proper error checking
- ✅ Test thoroughly with real API calls

---

## 📋 Complete List of Untyped Endpoints

### Empty Schema Endpoints (11)

These endpoints have **no response schema** defined in Elexon's OpenAPI specification.

#### 1. `get_cdn(format: Optional[str] = None) -> Dict[str, Any]`
**Endpoint:** `/CDN`  
**Status:** Deprecated  
**Description:** Credit default notices (moved to `/balancing/settlement/default-notices`)  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_cdn()
# result is Dict[str, Any] - no autocomplete!
# You must manually check the structure
```

---

#### 2. `get_demand(format: Optional[str] = None) -> Dict[str, Any]`
**Endpoint:** `/demand`  
**Description:** Summary of demand data  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_demand()
# result is Dict[str, Any]
# Check API docs for response structure
```

---

#### 3. `get_demand_rolling_system_demand(from_: str, to_: str, format: Optional[str] = None) -> Dict[str, Any]`
**Endpoint:** `/demand/rollingSystemDemand`  
**Description:** Rolling system demand  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_demand_rolling_system_demand(
    from_="2024-01-01",
    to_="2024-01-02"
)
# result is Dict[str, Any]
```

---

#### 4. `get_demand_summary(from_: str, to_: str, format: Optional[str] = None) -> Dict[str, Any]`
**Endpoint:** `/demand/summary`  
**Description:** Summary of all demand data  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_demand_summary(
    from_="2024-01-01",
    to_="2024-01-02"
)
# result is Dict[str, Any]
```

---

#### 5. `get_demand_total_actual(from_: str, to_: str, format: Optional[str] = None) -> Dict[str, Any]`
**Endpoint:** `/demand/total/actual`  
**Description:** Total actual demand  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_demand_total_actual(
    from_="2024-01-01",
    to_="2024-01-02"
)
# result is Dict[str, Any]
```

---

#### 6. `get_generation_outturn_half_hourly_interconnector(from_: str, to_: str, format: Optional[str] = None) -> Dict[str, Any]`
**Endpoint:** `/generation/outturn/halfHourlyInterconnector`  
**Description:** Half-hourly interconnector generation  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_generation_outturn_half_hourly_interconnector(
    from_="2024-01-01",
    to_="2024-01-02"
)
# result is Dict[str, Any]
```

---

#### 7. `get_generation_outturn_fuelinsthhcur(format: Optional[str] = None) -> Dict[str, Any]`
**Endpoint:** `/generation/outturn/FUELINSTHHCUR`  
**Description:** Current half-hourly generation by fuel type  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_generation_outturn_fuelinsthhcur()
# result is Dict[str, Any]
```

---

#### 8. `get_health() -> Dict[str, Any]`
**Endpoint:** `/health`  
**Description:** Health check endpoint  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_health()
# result is Dict[str, Any]
# Likely returns: {"status": "healthy"} or similar
```

---

#### 9. `get_interop_message_list_retrieval(...) -> Dict[str, Any]`
**Endpoint:** `/interop/MessageListRetrieval`  
**Description:** Legacy interop message list retrieval  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_interop_message_list_retrieval(...)
# result is Dict[str, Any]
```

---

#### 10. `get_interop_message_detail_retrieval(...) -> Dict[str, Any]`
**Endpoint:** `/interop/MessageDetailRetrieval`  
**Description:** Legacy interop message detail retrieval  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_interop_message_detail_retrieval(...)
# result is Dict[str, Any]
```

---

#### 11. `get_lolpdrm_forecast_evolution(...) -> Dict[str, Any]`
**Endpoint:** `/lolpdrm/forecast/evolution`  
**Description:** Loss of load probability de-rated margin forecast evolution  
**Warning:** ⚠️ Untyped response - no schema available

```python
# Usage
result = client.get_lolpdrm_forecast_evolution(...)
# result is Dict[str, Any]
```

---

### Stream Endpoint (1)

#### 12. `get_demand_stream(format: Optional[str] = None) -> Dict[str, Any]`
**Endpoint:** `/demand/stream`  
**Description:** Streaming demand data  
**Note:** This endpoint returns **streaming data** (Server-Sent Events or similar)

```python
# Usage
result = client.get_demand_stream()
# result is Dict[str, Any] - streaming data format
# Dict is appropriate for dynamic streaming responses
```

---

## 🛡️ Best Practices for Untyped Endpoints

### 1. Add Type Annotations in Your Code

```python
from typing import Any, Dict

def get_health_status(client: BMRSClient) -> Dict[str, Any]:
    """Wrapper with explicit typing."""
    result: Dict[str, Any] = client.get_health()
    return result
```

### 2. Validate Response Structure

```python
result = client.get_demand()

# Validate structure before use
if isinstance(result, dict):
    if 'data' in result:
        data = result['data']
        # Process data...
    else:
        print("Unexpected response structure!")
```

### 3. Add Error Handling

```python
try:
    result = client.get_health()
    status = result.get('status', 'unknown')
except Exception as e:
    print(f"Error calling health endpoint: {e}")
```

### 4. Document Expected Structure

```python
def fetch_demand_summary(client: BMRSClient) -> Dict[str, Any]:
    """
    Fetch demand summary.
    
    Returns:
        Dict with structure (expected):
        {
            'data': [...],
            'metadata': {...}
        }
    
    Note: This endpoint is untyped - structure not guaranteed!
    """
    return client.get_demand_summary(
        from_="2024-01-01",
        to_="2024-01-02"
    )
```

---

## 📝 How to Check Warnings

### In Your IDE

When you hover over or autocomplete these methods, you'll see the warning:

```
⚠️  WARNING: This endpoint returns untyped Dict[str, Any]
The OpenAPI specification does not define a response schema for this endpoint.
You will not get type checking or IDE autocomplete for the response.
```

### Using `help()`

```python
from elexon_bmrs import BMRSClient

client = BMRSClient()
help(client.get_health)

# Output shows:
# ⚠️  WARNING: This endpoint returns untyped Dict[str, Any]
# ...
```

---

## 🔮 Future Improvements

To make these endpoints typed, we need **Elexon to update the OpenAPI specification** with proper response schemas.

**How you can help:**
1. Contact Elexon API support
2. Request schema definitions for these 11 endpoints
3. We'll update the SDK immediately when schemas are added!

**Contact Elexon:**
- API Documentation: https://bmrs.elexon.co.uk/api-documentation
- Support Portal: https://www.elexonportal.co.uk/

---

## ✅ Recommended Alternatives

Many of these untyped endpoints have **typed alternatives** you should prefer:

| Untyped Endpoint | Typed Alternative | Status |
|------------------|-------------------|--------|
| `get_cdn()` | `get_balancing_settlement_default_notices()` | ✅ Use this instead |
| `get_demand()` | `get_demand_outturn_daily()` | ✅ Fully typed |
| `get_generation_outturn_fuelinsthhcur()` | `get_generation_actual_per_type()` | ✅ Fully typed |

**Always prefer typed endpoints when available!**

---

## 📊 Summary

- **275 endpoints (95%)** are fully typed ✅
- **12 endpoints (4%)** are untyped ⚠️
- **11 untyped** due to missing OpenAPI schemas
- **1 untyped** because it streams data
- **All untyped endpoints have clear warnings** in docstrings

**Use typed endpoints whenever possible for the best development experience!**

---

## 🔍 Quick Reference

```python
# ✅ TYPED - Great developer experience
result = client.get_balancing_dynamic(...)
for item in result.data:  # Autocomplete works!
    print(item.dataset, item.value)

# ⚠️ UNTYPED - Manual structure handling
result = client.get_health()  # Dict[str, Any]
if 'status' in result:  # No autocomplete
    print(result['status'])
```

**When in doubt, use `help(client.method_name)` to check if it's typed!**

