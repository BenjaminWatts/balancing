# Code Generation

This project uses automated code generation from the OpenAPI specification.

## Overview

The library includes tools to automatically generate:

- Client methods from OpenAPI spec
- Pydantic models (280 models with 100% coverage)
- Type hints and documentation

## Generating Code

```bash
# Download latest OpenAPI spec
make download-schema

# Generate client methods
make generate

# Generate Pydantic models
make generate-models

# Generate everything
make generate-all
```

## Validation

Validate existing client against spec:

```bash
make validate-client
```

For detailed documentation, see [tools/README.md](https://github.com/benjaminwatts/balancing/blob/main/tools/README.md).
