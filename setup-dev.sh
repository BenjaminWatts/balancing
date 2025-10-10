#!/bin/bash
# Setup development environment with pre-commit hooks

set -e

echo "Setting up development environment..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "Pre-commit hooks installed:"
echo "  - trailing-whitespace"
echo "  - end-of-file-fixer"
echo "  - check-yaml, check-json, check-toml"
echo "  - black (code formatting)"
echo "  - flake8 (linting)"
echo "  - isort (import sorting)"
echo "  - mypy (type checking)"
echo "  - pytest (unit tests)"
echo ""
echo "Hooks will run automatically on 'git commit'"
echo "To run manually: pre-commit run --all-files"
echo ""
echo "To skip hooks (not recommended): git commit --no-verify"

