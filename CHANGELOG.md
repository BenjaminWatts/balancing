# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **287 API endpoints** - Complete coverage of all BMRS data via inheritance from GeneratedBMRSMethods
- **Complete documentation** with MkDocs Material theme
  - Auto-generated API reference from docstrings
  - Comprehensive endpoint reference page listing all 287 methods
  - Examples and guides for all major use cases
  - Automatic deployment to GitHub Pages
- Complete PyPI distribution setup with comprehensive guide
- 280 auto-generated Pydantic models (100% OpenAPI schema coverage)
- API key optionality documentation and runtime warnings
- Type safety with full IDE autocomplete support
- Specific response types for each endpoint (SystemDemandResponse, GenerationResponse, etc.)
- Comprehensive examples (basic, typed, advanced usage)
- Pre-release checklist and automation (`make pre-release`)
- TestPyPI testing workflow
- PEP 561 type information marker file (`py.typed`)
- Documentation build commands (`make docs`, `make docs-serve`, `make docs-deploy`)
- GitHub Actions workflow for automatic documentation deployment

### Changed
- Improved API key documentation (optional but strongly recommended)
- Enhanced MANIFEST.in to include all necessary files
- Updated Makefile with PyPI distribution commands
- Better project metadata in pyproject.toml

### Fixed
- Duplicate class names from wrapper types (280 models vs. 142)
- Intelligent suffix strategy for wrapper types

## [0.1.0] - TBD

### Added
- Initial release
- Full BMRS API client with 100+ endpoints
- Rate limiting support with RateLimitError
- Comprehensive error handling
- Type hints throughout
- Context manager support
- Examples and documentation

### Features
- 🔌 Simple and intuitive API interface
- 🔑 API key optional (but recommended for higher rate limits)
- 📊 Access to comprehensive UK electricity market data
- 🔄 Support for multiple data streams (generation, demand, pricing, etc.)
- ⚡ Specific response type for each endpoint
- 🛡️ Built-in error handling and validation
- 📝 Full type hints and IDE autocomplete
- 🤖 Auto-generated models from OpenAPI specification (280 models)
- 🧪 Comprehensive test coverage

---

## Version History

- **[Unreleased]**: Work in progress for next release
- **[0.1.0]**: Initial release (TBD)

## Links

- [PyPI Package](https://pypi.org/project/elexon-bmrs/)
- [GitHub Repository](https://github.com/benjaminwatts/elexon-bmrs)
- [Documentation](https://github.com/benjaminwatts/elexon-bmrs#readme)
- [Issue Tracker](https://github.com/benjaminwatts/elexon-bmrs/issues)

