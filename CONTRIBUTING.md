# Contributing to Elexon BMRS Python Client

Thank you for your interest in contributing to the Elexon BMRS Python Client! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (Python version, OS, etc.)
- Any relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

- A clear description of the enhancement
- Use cases and benefits
- Potential implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/benjaminwatts/elexon-bmrs.git
   cd elexon-bmrs
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

4. **Make your changes**
   - Write clear, readable code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

5. **Run tests and checks**
   ```bash
   # Run tests
   pytest
   
   # Check code formatting
   black elexon_bmrs tests examples
   isort elexon_bmrs tests examples
   
   # Run linter
   flake8 elexon_bmrs tests examples
   
   # Type checking
   mypy elexon_bmrs
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

   Use clear commit messages:
   - `Add: new feature or functionality`
   - `Fix: bug fix`
   - `Update: modifications to existing features`
   - `Docs: documentation changes`
   - `Test: adding or updating tests`
   - `Refactor: code restructuring`

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Provide a clear description of your changes
   - Reference any related issues

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

### Testing

- Write tests for all new functionality
- Aim for high test coverage (>80%)
- Use pytest for testing
- Mock external API calls in tests

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions and classes
- Update examples if adding new functionality
- Keep CHANGELOG.md up to date

### Commit Guidelines

- Keep commits atomic (one logical change per commit)
- Write clear, concise commit messages
- Reference issue numbers in commits when applicable

## Project Structure

```
elexon-bmrs/
├── elexon_bmrs/          # Main package
│   ├── __init__.py       # Package initialization
│   ├── client.py         # Main client class
│   ├── exceptions.py     # Custom exceptions
│   └── models.py         # Data models
├── tests/                # Test suite
│   ├── test_client.py    # Client tests
│   └── test_exceptions.py # Exception tests
├── examples/             # Usage examples
│   ├── basic_usage.py    # Basic examples
│   └── advanced_usage.py # Advanced examples
├── pyproject.toml        # Project metadata
├── setup.py              # Setup script
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Reach out to the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in the project's README and release notes.

Thank you for contributing! 🎉

