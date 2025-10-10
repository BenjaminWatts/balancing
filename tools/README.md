# BMRS Client Code Generation Tools

This directory contains tools for automating the generation and validation of BMRS API client code based on the official OpenAPI specification.

## Tools Overview

### 1. `download_schema.py`
Downloads the latest OpenAPI specification from the Elexon BMRS API.

```bash
python tools/download_schema.py
```

**What it does:**
- Attempts to download the OpenAPI spec from known BMRS API documentation URLs
- Validates that the downloaded file is a valid OpenAPI specification
- Saves the spec to `schema/bmrs_openapi.json`
- Prints a summary of available endpoints and data models

### 2. `generate_client.py`
Generates Python client methods from the OpenAPI specification.

```bash
python tools/generate_client.py
```

**What it does:**
- Reads the OpenAPI specification from `schema/bmrs_openapi.json`
- Generates Python methods for each API endpoint
- Creates proper type hints and docstrings
- Saves generated code to `elexon_bmrs/generated_client.py`

**Features:**
- Automatic method naming based on endpoint paths and operations
- Type-safe parameter handling
- Complete docstrings with parameter descriptions
- Handles path parameters, query parameters, and headers

### 3. `validate_client.py`
Validates and compares the existing client with the OpenAPI spec.

```bash
python tools/validate_client.py
```

**What it does:**
- Compares manually written client methods with spec endpoints
- Identifies missing endpoints that should be implemented
- Finds undocumented methods
- Compares existing client with generated client
- Suggests improvements and updates

**Validation checks:**
- ✓ Missing endpoints from the spec
- ✓ Methods without docstrings
- ✓ Differences between manual and generated code
- ✓ Parameter mismatches

## Workflow

### Initial Setup

1. **Download the API specification:**
   ```bash
   python tools/download_schema.py
   ```

2. **Generate client code:**
   ```bash
   python tools/generate_client.py
   ```

3. **Validate existing implementation:**
   ```bash
   python tools/validate_client.py
   ```

### Regular Updates

Run these scripts periodically to keep your client up-to-date:

```bash
# Download latest spec
python tools/download_schema.py

# Regenerate client
python tools/generate_client.py

# Check for conflicts
python tools/validate_client.py
```

### Integration Workflow

1. Review generated code in `elexon_bmrs/generated_client.py`
2. Compare with existing code in `elexon_bmrs/client.py`
3. Identify new endpoints or changes
4. Manually integrate changes, adding custom logic as needed
5. Update tests accordingly

## Manual vs Generated Code

### When to use generated code:
- Initial client creation
- Adding support for new endpoints
- Ensuring completeness of API coverage
- Maintaining consistency with API specification

### When to write manual code:
- Custom error handling
- Data transformation and validation
- Business logic specific to your use case
- Convenience methods combining multiple API calls
- Adding caching or rate limiting

## Best Practices

1. **Keep generated code separate:** Don't edit `generated_client.py` directly
2. **Use inheritance or composition:** Extend generated methods in your main client
3. **Version control:** Commit both manual and generated code
4. **Document customizations:** Clearly mark custom code in your client
5. **Regular updates:** Run validation weekly or after API updates

## Troubleshooting

### Schema download fails
- Check your internet connection
- Verify the BMRS API documentation URL is correct
- Try manually downloading from: https://bmrs.elexon.co.uk/api-documentation/
- Check if the API requires authentication

### Generation produces errors
- Ensure the schema file is valid JSON
- Check OpenAPI version compatibility (supports 3.0+)
- Review error messages for specific issues

### Validation shows many differences
- This is normal if the API has changed
- Review each difference to determine if it's:
  - A new endpoint to add
  - A deprecated endpoint to remove
  - A parameter change to update

## Dependencies

Required Python packages:
```bash
pip install requests pyyaml  # For schema download
```

All other functionality uses Python standard library.

## Example Output

### download_schema.py
```
╔══════════════════════════════════════════════════════════╗
║            BMRS OpenAPI Specification Downloader         ║
╚══════════════════════════════════════════════════════════╝

Attempting to download from: https://bmrs.elexon.co.uk/api-documentation/openapi.json
✓ Successfully downloaded OpenAPI spec from https://bmrs.elexon.co.uk/api-documentation/openapi.json

✓ Saved OpenAPI specification to: schema/bmrs_openapi.json

============================================================
OpenAPI Specification Summary
============================================================
Title: Elexon BMRS API
Version: 1.0.0
Description: Balancing Mechanism Reporting Service API

Endpoints: 45

Sample endpoints:
  - /balancing/settlement/system-prices [get]
  - /datasets/B1620 [get]
  - /generation/actual/per-type [get]
  ... and 42 more

Data Models/Schemas: 23
============================================================
```

## Contributing

When adding new tools:
1. Follow the existing code structure
2. Add comprehensive docstrings
3. Include error handling
4. Update this README
5. Add examples of usage

## License

These tools are part of the elexon-bmrs package and share the same MIT license.


