# Installation

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Install from PyPI

The simplest way to install the Elexon BMRS client:

```bash
pip install elexon-bmrs
```

## Install from Source

For development or to get the latest changes:

```bash
# Clone the repository
git clone https://github.com/benjaminwatts/balancing.git
cd balancing

# Install in development mode
pip install -e .
```

## Install with Development Dependencies

If you want to contribute or run tests:

```bash
# Clone and navigate to repository
git clone https://github.com/benjaminwatts/balancing.git
cd balancing

# Install with dev dependencies
pip install -e ".[dev]"

# Or install dev dependencies separately
pip install -r requirements-dev.txt
```

## Verify Installation

Check that the installation was successful:

```bash
python -c "from elexon_bmrs import BMRSClient; print('✓ Installation successful!')"
```

You should see:
```
✓ Installation successful!
```

## Virtual Environment (Recommended)

It's recommended to use a virtual environment:

### Using venv

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install the package
pip install elexon-bmrs
```

### Using conda

```bash
# Create conda environment
conda create -n bmrs python=3.11

# Activate environment
conda activate bmrs

# Install the package
pip install elexon-bmrs
```

## Dependencies

The package automatically installs these core dependencies:

- **requests** - HTTP client for API calls
- **python-dateutil** - Date/time handling
- **pydantic** - Data validation and type hints

Development dependencies include:

- **pytest** - Testing framework
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking
- **mkdocs-material** - Documentation

## Troubleshooting

### SSL Certificate Errors

If you encounter SSL certificate errors:

```python
from elexon_bmrs import BMRSClient

# Disable SSL verification (not recommended for production)
client = BMRSClient(api_key="your-key", verify_ssl=False)
```

### Import Errors

If you get import errors, ensure you're in the correct Python environment:

```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list | grep elexon-bmrs
```

### Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade elexon-bmrs
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Start using the client
- [Authentication](authentication.md) - Set up your API key
- [API Reference](../api/client.md) - Detailed API documentation

