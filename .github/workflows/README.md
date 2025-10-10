# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the elexon-bmrs project.

## Workflows

### 1. Tests (`test.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`

**What it does:**
- ✅ Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- ✅ Code coverage reporting (Codecov)
- ✅ Linting (Black, isort, flake8)
- ✅ Type checking (mypy)
- ✅ Build verification

**Status Badge:**
```markdown
![Tests](https://github.com/benjaminwatts/elexon-bmrs/workflows/Tests/badge.svg)
```

### 2. Publish to PyPI (`publish.yml`)

**Triggers:**
- **Automatic**: When a GitHub Release is published
- **Manual**: Via workflow dispatch (Actions tab)

**What it does:**
- ✅ Builds distribution packages (wheel + sdist)
- ✅ Validates package integrity
- ✅ Publishes to TestPyPI or PyPI
- ✅ Uses trusted publishing (no API tokens needed!)

**Status Badge:**
```markdown
![Publish](https://github.com/benjaminwatts/elexon-bmrs/workflows/Publish%20to%20PyPI/badge.svg)
```

## Setup Instructions

### 1. Enable Trusted Publishing (Recommended)

Trusted Publishing is the modern, secure way to publish to PyPI without API tokens.

#### For PyPI (Production):

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `elexon-bmrs`
   - **Owner**: `benjaminwatts` (your GitHub username)
   - **Repository name**: `elexon-bmrs`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
4. Click "Add"

#### For TestPyPI (Testing):

1. Go to https://test.pypi.org/manage/account/publishing/
2. Repeat the same steps as above, but use:
   - **Environment name**: `testpypi`

### 2. Configure GitHub Environments (Optional but Recommended)

1. Go to your repository Settings → Environments
2. Create two environments:
   - **`testpypi`**: For testing releases
   - **`pypi`**: For production releases
3. For the `pypi` environment, add protection rules:
   - ✅ Required reviewers (yourself)
   - ✅ Wait timer (optional, e.g., 5 minutes to allow cancellation)

### 3. Alternative: Using API Tokens (Legacy Method)

If you prefer not to use trusted publishing:

1. Generate API tokens:
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/

2. Add them as GitHub Secrets:
   - Go to repository Settings → Secrets → Actions
   - Add secrets:
     - `PYPI_API_TOKEN` (for PyPI)
     - TEST_PYPI_API_TOKEN` (for TestPyPI)

3. Modify `publish.yml` to use tokens instead of trusted publishing:
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

## Usage

### Publishing a New Release

#### Method 1: GitHub Release (Automatic - Recommended)

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "0.1.0"
   ```

2. **Update** `CHANGELOG.md`

3. **Commit and push**:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Release v0.1.0"
   git push origin main
   ```

4. **Create a git tag**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

5. **Create a GitHub Release**:
   - Go to: https://github.com/benjaminwatts/elexon-bmrs/releases/new
   - Tag: `v0.1.0`
   - Title: `v0.1.0`
   - Description: Copy from CHANGELOG.md
   - Click "Publish release"

6. **Watch the workflow**:
   - Go to Actions tab
   - The "Publish to PyPI" workflow will run automatically
   - It will publish to PyPI when complete!

#### Method 2: Manual Trigger

1. Go to: https://github.com/benjaminwatts/elexon-bmrs/actions/workflows/publish.yml
2. Click "Run workflow"
3. Choose:
   - Branch: `main`
   - Environment: `testpypi` or `pypi`
4. Click "Run workflow"

### Testing Before Production Release

**Always test on TestPyPI first!**

1. Use manual trigger with `testpypi` environment
2. Wait for workflow to complete
3. Test installation:
   ```bash
   pip install -i https://test.pypi.org/simple/ \
       --extra-index-url https://pypi.org/simple \
       elexon-bmrs
   ```
4. Verify it works:
   ```bash
   python -c "from elexon_bmrs import BMRSClient; print('✓')"
   ```
5. If successful, create a GitHub Release for production

## Workflow Behavior

### Test Workflow

- **Runs on every push** to `main`/`develop`
- **Runs on every PR** to `main`
- Tests across Python 3.8-3.12
- Fast feedback (~5-10 minutes)

### Publish Workflow

- **Automatic trigger**: GitHub Release published → PyPI
- **Manual trigger**: You choose TestPyPI or PyPI
- Always builds fresh packages
- Always validates before publishing
- Idempotent (safe to re-run)

## Security Features

### ✅ Trusted Publishing
- No API tokens in GitHub Secrets
- Uses OpenID Connect (OIDC)
- PyPI verifies the workflow identity
- Most secure method available

### ✅ Environment Protection
- Production environment can require approval
- Prevents accidental releases
- Can add wait timers

### ✅ Read-only by Default
- Workflows have minimal permissions
- Only `id-token: write` for publishing
- Follows principle of least privilege

## Monitoring

### Check Workflow Status

1. **Actions Tab**: https://github.com/benjaminwatts/elexon-bmrs/actions
2. **Badges**: Add to README.md
3. **Email Notifications**: GitHub sends on failure

### View Published Packages

- **PyPI**: https://pypi.org/project/elexon-bmrs/
- **TestPyPI**: https://test.pypi.org/project/elexon-bmrs/

## Troubleshooting

### "Trusted publishing not configured"

**Solution**: Complete the Trusted Publishing setup (see above)

### "Package already exists"

**Solution**: Bump version in `pyproject.toml` - PyPI doesn't allow overwriting

### "Build failed"

**Solution**: Run locally first:
```bash
make pre-release  # Run all checks
make build        # Test build
```

### "Tests failing"

**Solution**: 
```bash
make test         # Run tests locally
make lint         # Check linting
make type-check   # Check types
```

### "Manual trigger not working"

**Solution**: Ensure you have write access to the repository

## Best Practices

### Before Every Release

1. ✅ Run `make pre-release` locally
2. ✅ Update `CHANGELOG.md`
3. ✅ Bump version in `pyproject.toml`
4. ✅ Test on TestPyPI first
5. ✅ Create git tag
6. ✅ Create GitHub Release

### Versioning

Follow Semantic Versioning:
- `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### Release Notes

Always include in GitHub Release description:
- What's new
- What changed
- What was fixed
- Breaking changes (if any)
- Migration guide (if needed)

## Comparing Approaches

### GitHub Actions vs Manual Publishing

| Feature | GitHub Actions | Manual (`make upload`) |
|---------|---------------|------------------------|
| **Speed** | ⚡ Fast | 🐌 Slower |
| **Consistency** | ✅ Always same | ⚠️ Varies |
| **Security** | ✅ Trusted publishing | ⚠️ Needs tokens |
| **Tracking** | ✅ Full history | ❌ No tracking |
| **Rollback** | ✅ Easy | ❌ Manual |
| **Collaboration** | ✅ Team friendly | ⚠️ Individual |
| **Testing** | ✅ Automatic | ⚠️ Manual |

**Recommendation**: Use GitHub Actions for production, keep `make upload` for emergency fixes.

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)

---

**Need Help?**
- Check workflow logs in Actions tab
- Review [PYPI_DISTRIBUTION.md](../../PYPI_DISTRIBUTION.md)
- Open an issue: https://github.com/benjaminwatts/elexon-bmrs/issues


