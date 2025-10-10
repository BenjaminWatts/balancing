# Rate Limiting

Guide to handling API rate limits effectively.

## Understanding Rate Limits

The Elexon BMRS API implements rate limiting to ensure fair usage. When exceeded, you'll receive a `429 Too Many Requests` error.

## Basic Rate Limit Handling

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import RateLimitError
import time

client = BMRSClient(api_key="your-key")

try:
    data = client.get_system_demand(from_date="2024-01-01", to_date="2024-01-02")
except RateLimitError as e:
    if e.retry_after:
        print(f"Waiting {e.retry_after} seconds...")
        time.sleep(e.retry_after)
    else:
        print("Rate limited. Implementing backoff...")
        time.sleep(60)
```

## Exponential Backoff

```python
import time
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import RateLimitError

def fetch_with_retry(client, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.get_system_demand(
                from_date="2024-01-01",
                to_date="2024-01-02"
            )
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = e.retry_after if e.retry_after else (2 ** attempt)
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
```

## Best Practices

1. **Use an API Key** - Higher rate limits with authentication
2. **Implement Backoff** - Wait progressively longer between retries
3. **Cache Responses** - Store frequently accessed data
4. **Batch Requests** - Use date ranges instead of individual requests
5. **Monitor Usage** - Track API calls in your application

For complete examples, see the [Advanced Examples](../examples/advanced.md) page.
