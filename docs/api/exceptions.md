# Exceptions API Reference

This page documents all exception classes used in the library.

## Base Exception

::: elexon_bmrs.exceptions.BMRSException
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Specific Exceptions

::: elexon_bmrs.exceptions.APIError
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

::: elexon_bmrs.exceptions.AuthenticationError
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

::: elexon_bmrs.exceptions.RateLimitError
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

::: elexon_bmrs.exceptions.ValidationError
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Usage Examples

### Handling API Errors

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import APIError

try:
    client = BMRSClient(api_key="your-key")
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
except APIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Response: {e.response}")
```

### Handling Authentication Errors

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import AuthenticationError

try:
    client = BMRSClient(api_key="invalid-key")
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
except AuthenticationError:
    print("Invalid API key. Please check your credentials.")
```

### Handling Rate Limits

```python
import time
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import RateLimitError

try:
    client = BMRSClient(api_key="your-key")
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
    if e.retry_after:
        time.sleep(e.retry_after)
```

### Handling Validation Errors

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import ValidationError

try:
    client = BMRSClient(api_key="your-key")
    # Invalid date format
    data = client.get_system_demand(
        from_date="invalid-date",
        to_date="2024-01-02"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Catching All BMRS Exceptions

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import BMRSException

try:
    client = BMRSClient(api_key="your-key")
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-02"
    )
except BMRSException as e:
    print(f"BMRS Error: {e}")
    # Handle all BMRS-related errors
```

