# Error Handling

Comprehensive guide to handling errors in the Elexon BMRS client.

## Exception Hierarchy

```
BMRSException (base)
├── APIError (general API errors)
├── AuthenticationError (invalid API key)
├── RateLimitError (rate limit exceeded)
└── ValidationError (invalid input)
```

## Specific Exceptions

### AuthenticationError

Raised when API authentication fails:

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import AuthenticationError

try:
    client = BMRSClient(api_key="invalid-key")
    data = client.get_system_demand(from_date="2024-01-01", to_date="2024-01-02")
except AuthenticationError as e:
    print("Invalid API key. Please check your credentials.")
```

### RateLimitError

Raised when rate limit is exceeded:

```python
from elexon_bmrs.exceptions import RateLimitError
import time

try:
    data = client.get_system_demand(from_date="2024-01-01", to_date="2024-01-02")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
    if e.retry_after:
        time.sleep(e.retry_after)
```

### ValidationError

Raised for invalid input parameters:

```python
from elexon_bmrs.exceptions import ValidationError

try:
    # Invalid settlement period (must be 1-50)
    data = client.get_market_index(settlement_date="2024-01-01", settlement_period=100)
except ValidationError as e:
    print(f"Validation error: {e}")
```

### APIError

General API errors:

```python
from elexon_bmrs.exceptions import APIError

try:
    data = client.get_system_demand(from_date="2024-01-01", to_date="2024-01-02")
except APIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Response: {e.response}")
```

## Comprehensive Error Handling

Handle all possible errors:

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    BMRSException
)

def fetch_data_safely(api_key: str, date: str):
    try:
        client = BMRSClient(api_key=api_key)
        return client.get_system_demand(from_date=date, to_date=date)
    
    except AuthenticationError:
        print("Authentication failed. Check your API key.")
        
    except ValidationError as e:
        print(f"Invalid parameters: {e}")
        
    except RateLimitError as e:
        print(f"Rate limited. Retry after {e.retry_after} seconds")
        
    except APIError as e:
        print(f"API error ({e.status_code}): {e}")
        
    except BMRSException as e:
        print(f"Unexpected BMRS error: {e}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
```

See [Rate Limiting Guide](rate-limiting.md) for detailed rate limit handling patterns.
