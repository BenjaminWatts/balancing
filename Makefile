.PHONY: help install install-dev test test-cov lint format type-check clean build check-build upload upload-test download-schema generate generate-models generate-all validate-client pre-release docs docs-serve docs-build docs-deploy

help:
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install         - Install package"
	@echo "  make install-dev     - Install package with dev dependencies"
	@echo "  make test            - Run tests"
	@echo "  make test-cov        - Run tests with coverage report"
	@echo "  make lint            - Run linter (flake8)"
	@echo "  make format          - Format code (black + isort)"
	@echo "  make type-check      - Run type checker (mypy)"
	@echo "  make clean           - Clean build artifacts"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs            - Build documentation"
	@echo "  make docs-serve      - Serve documentation locally"
	@echo "  make docs-build      - Build documentation (alias for docs)"
	@echo "  make docs-deploy     - Deploy documentation to GitHub Pages"
	@echo ""
	@echo "Code Generation:"
	@echo "  make download-schema - Download latest OpenAPI spec"
	@echo "  make generate        - Generate client from OpenAPI spec"
	@echo "  make generate-models - Generate Pydantic models from spec"
	@echo "  make generate-all    - Generate both client and models"
	@echo "  make validate-client - Validate client against spec"
	@echo ""
	@echo "PyPI Distribution:"
	@echo "  make build           - Build distribution packages (wheel + sdist)"
	@echo "  make check-build     - Check built packages for PyPI compliance"
	@echo "  make upload-test     - Upload to TestPyPI (for testing)"
	@echo "  make upload          - Upload to PyPI (production)"
	@echo "  make pre-release     - Run all checks before release"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

test:
	pytest

test-cov:
	pytest --cov=elexon_bmrs --cov-report=html --cov-report=term-missing

lint:
	flake8 elexon_bmrs tests examples

format:
	black elexon_bmrs tests examples
	isort elexon_bmrs tests examples

type-check:
	mypy elexon_bmrs

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	@echo "Building distribution packages..."
	python -m build
	@echo ""
	@echo "✓ Build complete!"
	@echo "  Packages created in dist/"
	@ls -lh dist/

check-build: build
	@echo "Checking distribution packages..."
	python -m twine check dist/*
	@echo ""
	@echo "Checking package contents..."
	tar -tzf dist/*.tar.gz | head -20
	@echo ""
	@echo "✓ Build check complete!"

upload-test: check-build
	@echo "⚠️  Uploading to TestPyPI..."
	@echo "You can test installation with:"
	@echo "  pip install -i https://test.pypi.org/simple/ elexon-bmrs"
	python -m twine upload --repository testpypi dist/*

upload: check-build
	@echo "⚠️  WARNING: About to upload to PyPI (production)!"
	@echo "This will publish version $$(python -c 'import tomli; f = open(\"pyproject.toml\", \"rb\"); data = tomli.load(f); print(data[\"project\"][\"version\"]); f.close()') to PyPI."
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		python -m twine upload dist/*; \
		echo "✓ Upload complete!"; \
	else \
		echo "Upload cancelled."; \
		exit 1; \
	fi

pre-release: clean
	@echo "Running pre-release checks..."
	@echo ""
	@echo "1. Formatting code..."
	@make format
	@echo ""
	@echo "2. Running linter..."
	@make lint
	@echo ""
	@echo "3. Type checking..."
	@make type-check
	@echo ""
	@echo "4. Running tests..."
	@make test
	@echo ""
	@echo "5. Building packages..."
	@make check-build
	@echo ""
	@echo "✓ All pre-release checks passed!"
	@echo ""
	@echo "Ready to publish! Next steps:"
	@echo "  1. Review CHANGELOG.md"
	@echo "  2. Update version in pyproject.toml"
	@echo "  3. Commit and tag release"
	@echo "  4. Run 'make upload-test' to test on TestPyPI"
	@echo "  5. Run 'make upload' to publish to PyPI"

download-schema:
	python tools/download_schema.py

generate:
	python tools/generate_client.py

generate-models:
	python tools/generate_models.py

generate-all: download-schema generate generate-models
	@echo "✓ Generated client methods and Pydantic models"

validate-client:
	python tools/validate_client.py

# Documentation commands
docs:
	@echo "Building documentation..."
	mkdocs build --clean --strict
	@echo "✓ Documentation built in site/"

docs-serve:
	@echo "Starting documentation server..."
	@echo "Documentation will be available at http://127.0.0.1:8000"
	mkdocs serve

docs-build: docs

docs-deploy:
	@echo "Deploying documentation to GitHub Pages..."
	mkdocs gh-deploy --force
	@echo "✓ Documentation deployed!"

all: format lint type-check test

