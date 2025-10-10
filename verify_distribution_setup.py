#!/usr/bin/env python3
"""
Verify PyPI distribution setup is correct.

This script checks that all required files and configurations
are in place for publishing to PyPI.
"""

import sys
from pathlib import Path

def check_file(filepath: str, description: str) -> bool:
    """Check if a file exists."""
    path = Path(filepath)
    if path.exists():
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} (MISSING)")
        return False

def check_content(filepath: str, content: str, description: str) -> bool:
    """Check if a file contains specific content."""
    path = Path(filepath)
    if not path.exists():
        print(f"✗ {description}: {filepath} (FILE MISSING)")
        return False
    
    try:
        text = path.read_text()
        if content in text:
            print(f"✓ {description}")
            return True
        else:
            print(f"✗ {description} (CONTENT MISSING)")
            return False
    except Exception as e:
        print(f"✗ {description}: Error reading file: {e}")
        return False

def main():
    """Run all checks."""
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "PyPI Distribution Setup Verification" + " " * 12 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    checks = []
    
    # Essential files
    print("Essential Files:")
    print("-" * 60)
    checks.append(check_file("README.md", "README"))
    checks.append(check_file("LICENSE", "License"))
    checks.append(check_file("pyproject.toml", "Build configuration"))
    checks.append(check_file("setup.py", "Setup script"))
    checks.append(check_file("MANIFEST.in", "Manifest"))
    checks.append(check_file("requirements.txt", "Requirements"))
    checks.append(check_file("requirements-dev.txt", "Dev requirements"))
    print()
    
    # Package structure
    print("Package Structure:")
    print("-" * 60)
    checks.append(check_file("elexon_bmrs/__init__.py", "Package __init__"))
    checks.append(check_file("elexon_bmrs/client.py", "Client module"))
    checks.append(check_file("elexon_bmrs/models.py", "Models module"))
    checks.append(check_file("elexon_bmrs/exceptions.py", "Exceptions module"))
    checks.append(check_file("elexon_bmrs/generated_models.py", "Generated models"))
    checks.append(check_file("elexon_bmrs/py.typed", "Type information marker"))
    print()
    
    # Documentation
    print("Documentation:")
    print("-" * 60)
    checks.append(check_file("CONTRIBUTING.md", "Contributing guide"))
    checks.append(check_file("PYPI_DISTRIBUTION.md", "PyPI distribution guide"))
    checks.append(check_file("CHANGELOG.md", "Changelog"))
    print()
    
    # Configuration files
    print("Configuration:")
    print("-" * 60)
    checks.append(check_file(".gitignore", "Git ignore"))
    checks.append(check_file(".pypirc.template", "PyPI config template"))
    checks.append(check_file("Makefile", "Make targets"))
    print()
    
    # Content checks
    print("Configuration Content:")
    print("-" * 60)
    checks.append(check_content(
        "pyproject.toml",
        "elexon-bmrs",
        "Package name in pyproject.toml"
    ))
    checks.append(check_content(
        "pyproject.toml",
        "version =",
        "Version in pyproject.toml"
    ))
    checks.append(check_content(
        "pyproject.toml",
        "readme =",
        "README reference in pyproject.toml"
    ))
    checks.append(check_content(
        "MANIFEST.in",
        "include README.md",
        "README in MANIFEST.in"
    ))
    checks.append(check_content(
        "MANIFEST.in",
        "include LICENSE",
        "LICENSE in MANIFEST.in"
    ))
    checks.append(check_content(
        "requirements-dev.txt",
        "build>=",
        "Build tool in dev requirements"
    ))
    checks.append(check_content(
        "requirements-dev.txt",
        "twine>=",
        "Twine tool in dev requirements"
    ))
    print()
    
    # Makefile targets
    print("Makefile Targets:")
    print("-" * 60)
    checks.append(check_content("Makefile", "build:", "Build target"))
    checks.append(check_content("Makefile", "check-build:", "Check-build target"))
    checks.append(check_content("Makefile", "upload-test:", "Upload-test target"))
    checks.append(check_content("Makefile", "upload:", "Upload target"))
    checks.append(check_content("Makefile", "pre-release:", "Pre-release target"))
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(checks)
    total = len(checks)
    print(f"\nResults: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ All checks passed! Package is ready for PyPI distribution.")
        print("\nNext steps:")
        print("  1. Install dev dependencies: pip install -e '.[dev]'")
        print("  2. Run pre-release checks: make pre-release")
        print("  3. Test on TestPyPI: make upload-test")
        print("  4. Publish to PyPI: make upload")
        print("\nSee PYPI_DISTRIBUTION.md for detailed instructions.")
        return 0
    else:
        print(f"\n✗ {total - passed} check(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

