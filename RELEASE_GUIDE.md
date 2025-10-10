# Release Guide: Publishing to PyPI

## Overview

The project uses **GitHub Actions** with **PyPI Trusted Publishing** for secure, automated releases. No API tokens needed!

## Workflow Triggers

The publish workflow (`.github/workflows/publish.yml`) triggers on:

1. **GitHub Release** (recommended) - Automatic
2. **Manual dispatch** - For testing

## Publishing Methods

### Method 1: GitHub Release (Recommended)

This is the standard way to publish a new version:

```bash
# 1. Update version in pyproject.toml
# version = "0.1.0"

# 2. Commit and push
git add pyproject.toml
git commit -m "chore: bump version to 0.1.0"
git push

# 3. Create a GitHub release
gh release create v0.1.0 \
  --title "v0.1.0 - Initial Release" \
  --notes "## Features

- 287 API endpoints with full coverage
- 22 enum types for type safety
- 47 mixin types (18 field + 29 method)
- 894 required fields (64%)
- Comprehensive validation
- Complete documentation

## Installation

\`\`\`bash
pip install elexon-bmrs
\`\`\`

See the [documentation](https://benjaminwatts.github.io/balancing/) for details."

# 4. Watch the workflow
gh run watch
```

The workflow will automatically:
- Build the package
- Run tests
- Publish to PyPI
- Update GitHub release with artifacts

### Method 2: Manual Workflow Dispatch

For testing or manual releases:

```bash
# Test on TestPyPI first
gh workflow run publish.yml -f environment=testpypi

# Then publish to PyPI
gh workflow run publish.yml -f environment=pypi

# Watch the workflow
gh run watch
```

## Setting Up PyPI Trusted Publishing

**Important:** You need to configure Trusted Publishing on PyPI BEFORE the first release.

### For First Release (Package Doesn't Exist Yet)

1. Go to **https://pypi.org/manage/account/publishing/**
2. Click **"Add a new pending publisher"**
3. Fill in:
   - **PyPI Project Name:** `elexon-bmrs`
   - **Owner:** `BenjaminWatts`
   - **Repository name:** `balancing`
   - **Workflow name:** `publish.yml`
   - **Environment name:** `pypi`
4. Click **"Add"**

### For Subsequent Releases (Package Exists)

Once the package is published, Trusted Publishing is automatically configured. Just create releases as normal.

## Release Checklist

Before creating a release:

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Run tests locally: `pytest tests/`
- [ ] Build docs locally: `mkdocs build --strict`
- [ ] Commit and push all changes
- [ ] Create GitHub release with tag
- [ ] Wait for workflow to complete
- [ ] Verify on PyPI: https://pypi.org/project/elexon-bmrs/
- [ ] Test installation: `pip install elexon-bmrs`

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backward compatible
- **Patch** (0.0.1): Bug fixes, backward compatible

### Examples

```bash
# First release
git tag v0.1.0

# Bug fix
git tag v0.1.1

# New features
git tag v0.2.0

# Breaking changes
git tag v1.0.0
```

## Workflow Details

### Build Job
1. Checkout code
2. Set up Python 3.11
3. Install build dependencies
4. Build distribution packages (`sdist` and `wheel`)
5. Check package integrity with `twine check`
6. Upload artifacts

### Publish to TestPyPI Job
- Runs on manual dispatch with `environment=testpypi`
- Uses Trusted Publishing (no token needed)
- URL: https://test.pypi.org/p/elexon-bmrs

### Publish to PyPI Job
- Runs on GitHub release OR manual dispatch with `environment=pypi`
- Uses Trusted Publishing (no token needed)
- URL: https://pypi.org/p/elexon-bmrs

## Testing Before Release

### Test Locally

```bash
# Install in development mode
pip install -e .

# Run tests
pytest tests/

# Build package
python -m build

# Check package
twine check dist/*
```

### Test on TestPyPI

```bash
# Publish to TestPyPI
gh workflow run publish.yml -f environment=testpypi

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ elexon-bmrs

# Test it works
python -c "from elexon_bmrs import BMRSClient; print('✅ Works!')"
```

## Monitoring

### Watch Workflow

```bash
# List recent runs
gh run list --workflow=publish.yml

# Watch current run
gh run watch

# View specific run
gh run view <run-id> --log
```

### Check PyPI

After successful publish:
- **PyPI page:** https://pypi.org/project/elexon-bmrs/
- **Install:** `pip install elexon-bmrs`
- **Stats:** https://pypistats.org/packages/elexon-bmrs

## Troubleshooting

### "Package already exists"
- Version already published
- Bump version number
- Can't republish same version

### "Trusted publishing not configured"
- Set up at https://pypi.org/manage/account/publishing/
- Add pending publisher for first release

### "Workflow failed"
- Check logs: `gh run view <run-id> --log-failed`
- Common issues: test failures, build errors, version conflicts

## Summary

**To publish a new release:**

```bash
# 1. Update version
# Edit pyproject.toml: version = "0.1.0"

# 2. Commit and push
git add pyproject.toml
git commit -m "chore: bump version to 0.1.0"
git push

# 3. Create release
gh release create v0.1.0 --title "v0.1.0" --notes "Release notes here"

# 4. Wait for workflow
gh run watch

# Done! Package published to PyPI ✅
```

**First time only:** Configure Trusted Publishing at https://pypi.org/manage/account/publishing/

No API tokens needed! 🎉

