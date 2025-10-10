# Publishing Guide

Guide for maintainers on publishing releases.

## Automated Publishing (Recommended)

Use GitHub Actions for automated PyPI publishing:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit changes
4. Create and push tag: `git tag v0.1.0 && git push origin v0.1.0`
5. Create GitHub Release
6. Automatic publish to PyPI! 🎉

See [GITHUB_ACTIONS_SETUP.md](https://github.com/benjaminwatts/balancing/blob/main/GITHUB_ACTIONS_SETUP.md) for setup.

## Manual Publishing

```bash
# Run pre-release checks
make pre-release

# Test on TestPyPI
make upload-test

# Publish to PyPI
make upload
```

For detailed instructions, see [PYPI_DISTRIBUTION.md](https://github.com/benjaminwatts/balancing/blob/main/PYPI_DISTRIBUTION.md).
