# Authentication

## Do I Need an API Key?

The API key is **optional but strongly recommended** by Elexon. While the API can function without a key, using one provides significant benefits:

✅ **Higher rate limits** - Avoid hitting rate limits during data retrieval  
✅ **Better performance** - Improved reliability and response times  
✅ **Usage tracking** - Monitor your API usage and get support  
✅ **Production ready** - Essential for any production application

## Getting Your API Key

### 1. Register at Elexon Portal

Visit the [Elexon Portal](https://www.elexonportal.co.uk/) and register for a free account.

### 2. Navigate to API Section

Once logged in, navigate to the API section in your account dashboard.

### 3. Generate API Key

Generate your API key and copy it to a secure location.

### 4. Keep it Secure

⚠️ **Important**: Never commit your API key to version control or share it publicly.

## Using Your API Key

### Direct Initialization

The simplest way to use your API key:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(api_key="your-api-key-here")
```

### Environment Variables (Recommended)

Store your API key in an environment variable for better security:

```bash
# Set environment variable
export BMRS_API_KEY="your-api-key-here"
```

Then in your Python code:

```python
import os
from elexon_bmrs import BMRSClient

# Read from environment variable
api_key = os.getenv("BMRS_API_KEY")
client = BMRSClient(api_key=api_key)
```

### Using .env File

For local development, use a `.env` file (never commit this file!):

```bash
# .env file
BMRS_API_KEY=your-api-key-here
```

Install python-dotenv:

```bash
pip install python-dotenv
```

Load in your code:

```python
import os
from dotenv import load_dotenv
from elexon_bmrs import BMRSClient

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("BMRS_API_KEY")
client = BMRSClient(api_key=api_key)
```

### Configuration File

For more complex setups, use a configuration file:

```python
# config.py
import json
from pathlib import Path

def load_config():
    """Load configuration from JSON file."""
    config_path = Path.home() / ".bmrs" / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}

# Usage
config = load_config()
api_key = config.get("api_key")
```

## Using Without an API Key

You can use the client without an API key, but you'll see a warning:

```python
from elexon_bmrs import BMRSClient

# No API key provided - warning will be logged
client = BMRSClient()
```

Output:
```
⚠️  No API key provided. While the API may work without a key, 
Elexon strongly recommends using one for:
  • Higher rate limits
  • Better performance
  • Usage tracking and support
Get your free API key at: https://www.elexonportal.co.uk/
```

## Testing Authentication

Verify your API key works:

```python
from elexon_bmrs import BMRSClient
from elexon_bmrs.exceptions import AuthenticationError

try:
    client = BMRSClient(api_key="your-api-key")
    # Try a simple request
    data = client.get_system_demand(
        from_date="2024-01-01",
        to_date="2024-01-01"
    )
    print("✓ Authentication successful!")
except AuthenticationError:
    print("✗ Authentication failed - invalid API key")
```

## Security Best Practices

### 1. Never Hardcode API Keys

❌ **Bad:**
```python
client = BMRSClient(api_key="pk_live_1234567890abcdef")
```

✅ **Good:**
```python
import os
api_key = os.getenv("BMRS_API_KEY")
client = BMRSClient(api_key=api_key)
```

### 2. Add .env to .gitignore

Always exclude sensitive files from version control:

```gitignore
# .gitignore
.env
config.json
*.key
```

### 3. Use Different Keys for Different Environments

Maintain separate API keys for:

- Development
- Testing
- Production

### 4. Rotate Keys Regularly

Regularly regenerate your API keys for better security.

### 5. Monitor Usage

Check your API usage regularly in the Elexon Portal to detect any unauthorized use.

## Custom Base URL

For testing or alternative endpoints:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(
    api_key="your-api-key",
    base_url="https://custom-endpoint.example.com/api/v1"
)
```

## Advanced Configuration

Configure timeout and SSL verification:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(
    api_key="your-api-key",
    timeout=60,  # Request timeout in seconds
    verify_ssl=True  # SSL certificate verification
)
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Start using the client
- [Rate Limiting Guide](../guide/rate-limiting.md) - Handle rate limits
- [API Reference](../api/client.md) - Complete documentation

