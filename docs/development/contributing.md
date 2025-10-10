# Contributing

Contributions are welcome! This guide will help you get started.

## Development Setup

```bash
# Clone repository
git clone https://github.com/benjaminwatts/balancing.git
cd balancing

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"
pip install -r requirements-dev.txt
```

## Running Tests

```bash
# Run tests
pytest

# With coverage
pytest --cov=elexon_bmrs --cov-report=html
```

## Code Quality

```bash
# Format code
black elexon_bmrs tests
isort elexon_bmrs tests

# Lint
flake8 elexon_bmrs tests

# Type check
mypy elexon_bmrs
```

## Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and add tests
4. Run quality checks (`make pre-release`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

For more details, see [CONTRIBUTING.md](https://github.com/benjaminwatts/balancing/blob/main/CONTRIBUTING.md).
