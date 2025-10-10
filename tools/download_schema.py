"""
Script to download the Elexon BMRS API OpenAPI specification.

This script fetches the latest API schema from the BMRS API documentation
and saves it locally for code generation and validation.
"""

import json
import sys
from pathlib import Path
from typing import Optional
import requests


# Official BMRS API OpenAPI specification URL
# Based on: https://bmrs.elexon.co.uk/api-documentation/guidance
BMRS_OPENAPI_URL = "https://data.elexon.co.uk/bmrs/api/v1/docs/v1/openapi.json"

# Fallback URLs to try if the primary URL fails
FALLBACK_SPEC_URLS = [
    "https://data.elexon.co.uk/bmrs/api/v1/swagger.json",
    "https://bmrs.elexon.co.uk/api-documentation/openapi.json",
]


def download_openapi_spec(url: str, timeout: int = 30) -> Optional[dict]:
    """
    Download OpenAPI specification from a URL.

    Args:
        url: URL to download from
        timeout: Request timeout in seconds

    Returns:
        Parsed JSON/YAML spec or None if failed
    """
    try:
        print(f"Attempting to download from: {url}")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        # Try to parse as JSON
        if url.endswith(".json") or "application/json" in response.headers.get(
            "content-type", ""
        ):
            spec = response.json()
        else:
            # Try YAML if not JSON
            try:
                import yaml

                spec = yaml.safe_load(response.text)
            except ImportError:
                print("Warning: PyYAML not installed. Install with: pip install pyyaml")
                spec = response.json()

        # Validate it looks like an OpenAPI spec
        if "openapi" in spec or "swagger" in spec:
            print(f"✓ Successfully downloaded OpenAPI spec from {url}")
            return spec
        else:
            print(f"✗ Response doesn't appear to be an OpenAPI spec")
            return None

    except requests.RequestException as e:
        print(f"✗ Failed to download from {url}: {e}")
        return None
    except (json.JSONDecodeError, ValueError) as e:
        print(f"✗ Failed to parse response: {e}")
        return None


def save_spec(spec: dict, output_path: Path) -> None:
    """
    Save OpenAPI specification to file.

    Args:
        spec: OpenAPI specification dictionary
        output_path: Path to save the spec
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, sort_keys=True)

    print(f"\n✓ Saved OpenAPI specification to: {output_path}")


def print_spec_summary(spec: dict) -> None:
    """
    Print a summary of the OpenAPI specification.

    Args:
        spec: OpenAPI specification dictionary
    """
    print("\n" + "=" * 60)
    print("OpenAPI Specification Summary")
    print("=" * 60)

    info = spec.get("info", {})
    print(f"Title: {info.get('title', 'N/A')}")
    print(f"Version: {info.get('version', 'N/A')}")
    print(f"Description: {info.get('description', 'N/A')[:100]}...")

    # Count paths/endpoints
    paths = spec.get("paths", {})
    print(f"\nEndpoints: {len(paths)}")

    # List some example paths
    if paths:
        print("\nSample endpoints:")
        for i, (path, methods) in enumerate(list(paths.items())[:5]):
            method_list = ", ".join(methods.keys())
            print(f"  - {path} [{method_list}]")

        if len(paths) > 5:
            print(f"  ... and {len(paths) - 5} more")

    # Count schemas/models
    schemas = spec.get("components", {}).get("schemas", {})
    print(f"\nData Models/Schemas: {len(schemas)}")

    print("=" * 60)


def main() -> int:
    """Main entry point."""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "BMRS OpenAPI Specification Downloader" + " " * 9 + "║")
    print("╚" + "=" * 58 + "╝\n")

    # Determine output path
    script_dir = Path(__file__).parent
    output_path = script_dir.parent / "schema" / "bmrs_openapi.json"

    # Try to download from the official URL first, then fallbacks
    spec = download_openapi_spec(BMRS_OPENAPI_URL)
    
    if not spec:
        print("\nTrying fallback URLs...")
        for url in FALLBACK_SPEC_URLS:
            spec = download_openapi_spec(url)
            if spec:
                break

    if not spec:
        print("\n✗ Failed to download OpenAPI specification from any known URL.")
        print("\nPlease manually download the OpenAPI spec from:")
        print("  https://bmrs.elexon.co.uk/api-documentation/")
        print(f"\nAnd save it to: {output_path}")
        return 1

    # Handle spec wrapped in array
    if isinstance(spec, list) and len(spec) > 0:
        print("\nNote: Spec was wrapped in array, extracting first element")
        spec = spec[0]
    
    # Save the spec
    save_spec(spec, output_path)

    # Print summary
    print_spec_summary(spec)

    print("\n✓ Schema download complete!")
    print(f"\nNext steps:")
    print("  1. Review the schema: {output_path}")
    print("  2. Run: python tools/generate_client.py")
    print("  3. Run: python tools/validate_client.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())

