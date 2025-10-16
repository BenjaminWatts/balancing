# Changelog

All notable changes to the elexon-bmrs project will be documented in this file.

## [0.3.0] - 2024-10-16

### 🎉 Major Release: Full Type Safety

This release transforms the SDK into a fully typed Python client with 95% type coverage.

### Added
- **275 fully typed endpoints** (95% coverage) with Pydantic models
- **280 Pydantic models** auto-generated from OpenAPI spec
- **39 field mixins** to eliminate code duplication (~364+ lines saved)
- **Comprehensive test suite** (`tests/test_typed_endpoints.py`)
- **Clear warnings** for 12 untyped endpoints in docstrings
- **Type resolution** for List[Model], List[str], and wrapped responses
- **Automatic response parsing** with fallback to raw data
- **Documentation**: `UNTYPED_ENDPOINTS.md` for reference

### Changed
- All 287 methods now have proper return type annotations
- Generated client methods return Pydantic models instead of `Dict[str, Any]`
- Version bumped to 0.3.0
- User-Agent updated to `elexon-bmrs-python/0.3.0`

### Fixed
- PN endpoint model structure (fixed field definitions)
- BOALF endpoint model (corrected field mappings)
- Settlement stack model (added missing fields)
- URL construction in `_make_request`
- Import errors (removed obsolete `typed_client.py`)

### Removed
- `elexon_bmrs/typed_client.py` (typing now integrated in main client)
- `tools/generate_typed_client.py` (no longer needed)

### Technical Details
- **Type Coverage**: 275/287 endpoints (95%)
  - Single models: 181
  - List[Model]: 90
  - List[str]: 4
  - Untyped (Dict): 12 (API spec limitation)
- **Code Generation**: Fully automated from OpenAPI spec
- **Backward Compatible**: Zero breaking changes

### Documentation
- Added `UNTYPED_ENDPOINTS.md` - Complete reference for untyped endpoints
- Added in-code warnings for all untyped methods
- Updated all docstrings with proper return type documentation

## [0.2.0] - Previous Release

### Added
- BOALF endpoint support
- Physical Notifications (PN) endpoint
- Settlement stack methods
- Custom helper methods for common operations

### Fixed
- API endpoint URL construction
- Various model validation issues

## [0.1.0] - Initial Release

### Added
- Initial BMRS API client
- Basic endpoint coverage
- Exception handling
- API key support

