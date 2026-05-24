# Installation & Setup Guide

## Prerequisites

- Python 3.10+ (recommended 3.11)
- pip (Python package manager)
- Git
- Terminal/Command line access

## Step-by-Step Installation

### 1. Clone/Navigate to Project

```bash
cd playwright_api_framework
```

### 2. Quick Setup (Automated)

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Create necessary directories
- Create `.env` file from example

### 3. Manual Setup

If automated setup doesn't work:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Key configurations:**
- `TEST_ENV`: dev, staging, or production
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR
- `MAX_WORKERS`: Number of parallel workers (default: 4)
- `RETRY_ATTEMPTS`: Number of retries for flaky tests (default: 3)

### 5. Verify Installation

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run a quick test
pytest tests/test_posts_api.py::TestPostsAPI::test_get_all_posts -v
```

Expected output:
```
test_posts_api.py::TestPostsAPI::test_get_all_posts PASSED [100%]
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pytest'`
**Solution:** Ensure virtual environment is activated and dependencies are installed
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: `Timeout connecting to API`
**Solution:** Update timeout in `config/environments.yaml`
```yaml
dev:
  timeout: 15000  # Increase to 15 seconds
```

### Issue: Tests run sequentially instead of parallel
**Solution:** Ensure pytest-xdist is installed
```bash
pip install pytest-xdist --upgrade
```

### Issue: `Permission denied` for setup.sh
**Solution:** Make script executable
```bash
chmod +x setup.sh
./setup.sh
```

## Directory Structure After Setup

```
playwright_api_framework/
├── venv/                    # Virtual environment (created)
├── reports/                 # Test reports (created)
├── logs/                    # Test logs (created)
├── .env                     # Configuration (created from example)
├── config/
├── api/
├── utils/
├── data/
├── tests/
├── pytest.ini
├── requirements.txt
└── README.md
```

## IDE Setup

### VS Code

1. Install Python extension: `ms-python.python`
2. Open Command Palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
3. Select Python interpreter from venv:
   ```
   Python: Select Interpreter → ./venv/bin/python
   ```

### PyCharm

1. Open project settings: `PyCharm → Preferences → Project → Python Interpreter`
2. Click gear icon → Add
3. Select `Existing Environment`
4. Navigate to `./venv/bin/python`

## Next Steps

After successful installation:
1. Read [TESTING_GUIDE.md](TESTING_GUIDE.md) to learn how to run tests
2. Check [README.md](README.md) for API documentation
3. Explore `config/environments.yaml` to configure different environments
4. Review test examples in `tests/test_posts_api.py`

## Getting Help

- Check test logs: `tail -f logs/*.log`
- Run with debug logging: `pytest tests/ -v --log-cli-level=DEBUG`
- Review error messages in terminal output
- Check CI/CD logs for environment-specific issues

---

**Last Updated:** 2026-05-24  
**Framework:** Playwright + Python
