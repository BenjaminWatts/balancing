# Advanced Examples

Advanced patterns including error handling, retry logic, and rate limiting.

## Production Rate Limiting

```python
import time
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import RateLimitError, APIError

class RateLimitedClient:
    def __init__(self, api_key: str, max_retries: int = 3):
        self.client = BMRSClient(api_key=api_key)
        self.max_retries = max_retries
    
    def request_with_backoff(self, method, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return method(*args, **kwargs)
            except RateLimitError as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = e.retry_after if e.retry_after else (2 ** attempt)
                time.sleep(wait_time)
```

## Complete Examples

For full runnable examples, see:

- [examples/advanced_usage.py](https://github.com/benjaminwatts/balancing/blob/main/examples/advanced_usage.py)
