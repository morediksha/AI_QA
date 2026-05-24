# Testing Guide & Best Practices

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with parallel execution
pytest tests/ -v -n 4

# Run specific test file
pytest tests/test_posts_api.py -v

# Run with HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html
```

## Running Tests

### Basic Execution

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_posts_api.py

# Run specific test class
pytest tests/test_posts_api.py::TestPostsAPI

# Run specific test method
pytest tests/test_posts_api.py::TestPostsAPI::test_get_all_posts
```

### Parallel Execution

```bash
# Run with 4 workers (default)
pytest tests/ -n 4

# Run with specific number of workers
pytest tests/ -n 8

# Run with auto-detection of CPU cores
pytest tests/ -n auto

# Show which tests run on which worker
pytest tests/ -n 4 -v
```

### Filtering Tests

```bash
# Run only smoke tests
pytest tests/ -m smoke

# Run only regression tests
pytest tests/ -m regression

# Run only critical tests
pytest tests/ -m critical

# Run smoke OR regression tests
pytest tests/ -m "smoke or regression"

# Run tests excluding slow tests
pytest tests/ -m "not slow"

# Run tests by keyword
pytest tests/ -k "post" -v

# Run tests by keyword pattern
pytest tests/ -k "test_get" -v
```

### Retry & Resilience

```bash
# Retry failed tests (3 attempts)
pytest tests/ -v --reruns 3

# Retry with delay between attempts
pytest tests/ -v --reruns 3 --reruns-delay 2

# Stop after N failures
pytest tests/ -v --maxfail 3

# Stop on first failure
pytest tests/ -v -x
```

### Output & Reporting

```bash
# Generate HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html

# Generate Allure report
pytest tests/ -v --alluredir=reports/allure
allure serve reports/allure

# Generate JUnit XML (for CI/CD)
pytest tests/ -v --junitxml=reports/junit.xml

# Generate JSON report
pytest tests/ -v --json-report --json-report-file=reports/report.json

# Show only failures
pytest tests/ -v --tb=short

# Show no output (only summary)
pytest tests/ -q
```

### Debug & Logging

```bash
# Run with DEBUG logging
pytest tests/ -v --log-cli-level=DEBUG

# Show print statements
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -v -l

# Drop into debugger on failure
pytest tests/ -v --pdb

# Exit on first error
pytest tests/ -v -x
```

## Environment-Specific Testing

```bash
# Test against development environment
export TEST_ENV=dev
pytest tests/ -v

# Test against staging
export TEST_ENV=staging
pytest tests/ -v

# Test against production
export TEST_ENV=production
pytest tests/ -v

# Or use command line
pytest tests/ -v --override-ini="TEST_ENV=staging"
```

## Practical Test Scenarios

### Scenario 1: Quick Smoke Test
```bash
pytest tests/ -m smoke -v --tb=short
```

### Scenario 2: Full Regression with Reports
```bash
pytest tests/ -v -n 4 \
  --html=reports/report.html \
  --alluredir=reports/allure \
  --tb=short
```

### Scenario 3: Debug Failing Test
```bash
pytest tests/test_posts_api.py::TestPostsAPI::test_get_specific_post -v -s --log-cli-level=DEBUG
```

### Scenario 4: Run with Retry for Flaky Tests
```bash
pytest tests/ -v -n 4 --reruns 2 --reruns-delay 1
```

### Scenario 5: Test Specific API
```bash
pytest tests/test_posts_api.py -v
pytest tests/test_users_api.py -v
pytest tests/test_comments_api.py -v
```

## Parametrized Tests

Some tests include parametrization for testing multiple scenarios:

```python
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_multiple_users(self, users_api, user_id):
    """Tests will run for user_id = 1, 2, and 3"""
    ...
```

Run with details:
```bash
pytest tests/test_users_api.py::TestUsersAPI::test_get_multiple_users -v
```

## Custom Assertions

The framework includes custom assertion methods:

```python
from utils.assertions import APIAssertions

# Status code assertion
APIAssertions.assert_status_code(200, expected=200)

# Response contains keys
APIAssertions.assert_response_contains_keys(response, ["id", "name"])

# Specific field value
APIAssertions.assert_response_field(response, "status", "active")

# Response not empty
APIAssertions.assert_response_not_empty(response)

# Response is list
APIAssertions.assert_response_is_list(response, min_length=1)

# Response type check
APIAssertions.assert_response_type(response, dict)
```

## Writing New Tests

### Test Template

```python
import pytest
from utils.assertions import APIAssertions
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.api
@pytest.mark.regression
class TestNewAPI:
    """Test suite for New API"""
    
    @pytest.mark.smoke
    def test_api_endpoint(self, api_client):
        """Test: Description of what is being tested"""
        # Arrange
        expected_status = 200
        
        # Act
        response = api_client.get("/endpoint")
        
        # Assert
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_contains_keys(response, ["id", "name"])
        
        logger.info("Test passed successfully")
```

### Best Practices

1. **Use descriptive test names**
   ```python
   def test_create_post_with_valid_data(self):  # ✓ Good
   def test_create(self):                        # ✗ Poor
   ```

2. **Follow AAA pattern** (Arrange, Act, Assert)
   ```python
   def test_example(self, api_client):
       # Arrange
       payload = {"title": "Test"}
       
       # Act
       response = api_client.create(payload)
       
       # Assert
       assert response["id"] is not None
   ```

3. **Use fixtures for setup/teardown**
   ```python
   @pytest.fixture
   def setup_data(self):
       data = create_test_data()
       yield data
       cleanup_test_data(data)
   ```

4. **Mark tests appropriately**
   ```python
   @pytest.mark.smoke       # Quick sanity checks
   @pytest.mark.regression  # Full regression suite
   @pytest.mark.slow        # Long-running tests
   @pytest.mark.critical    # Must-pass tests
   ```

5. **Log important operations**
   ```python
   logger.info(f"Created post with ID: {response['id']}")
   logger.warning("Unexpected response field value")
   ```

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Daily schedule (2 AM UTC)

View results:
1. Go to GitHub repository
2. Click "Actions" tab
3. Select workflow run
4. Download artifacts for reports

### Jenkins

Run pipeline:
```groovy
stage('Test') {
    steps {
        sh 'pytest tests/ -v -n 4 --junitxml=reports/junit.xml'
        junit 'reports/junit.xml'
        archiveArtifacts artifacts: 'reports/**'
    }
}
```

## Troubleshooting Test Failures

### Issue: `Connection timeout`
```bash
# Increase timeout in .env
RETRY_ATTEMPTS=5
RETRY_DELAY=2
```

### Issue: `Test passes locally but fails in CI`
```bash
# Run with same environment as CI
docker build -t test-image .
docker run --rm test-image pytest tests/ -v
```

### Issue: `Flaky test (passes sometimes, fails sometimes)`
```bash
# Run with retry
pytest tests/ -v --reruns 3

# Check test logs
tail -f logs/*.log

# Mark as flaky temporarily
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_flaky_endpoint(self):
    ...
```

### Issue: `Tests run sequentially despite -n flag`
```bash
# Verify pytest-xdist is installed
pip list | grep xdist

# Reinstall if needed
pip install pytest-xdist --upgrade

# Check for xfail markers blocking parallelization
pytest tests/ -v -n 4 --verbose
```

## Test Reports

### HTML Report
```bash
pytest tests/ --html=reports/report.html --self-contained-html
# Open: reports/report.html
```

### Allure Report
```bash
pytest tests/ --alluredir=reports/allure
allure serve reports/allure
# Opens in browser automatically
```

### JUnit XML (for CI/CD)
```bash
pytest tests/ --junitxml=reports/junit.xml
# Use in Jenkins, GitLab CI, etc.
```

## Performance Optimization

```bash
# Profile test execution
pytest tests/ -v --durations=10

# Run only fast tests
pytest tests/ -m "not slow" -v

# Parallel with 8 workers
pytest tests/ -n 8 -v

# Combine optimizations
pytest tests/ -m "not slow" -n 8 --tb=short -q
```

---

**Last Updated:** 2026-05-24  
**Framework:** Playwright + Python
