# Playwright API Automation Framework

A production-ready automation framework for testing RESTful APIs using Playwright with Python. Designed with scalability, maintainability, and parallel execution in mind.

## Features

- ✅ **API Object Model** - Organized, reusable API client classes
- ✅ **Parallel Execution** - Built-in pytest-xdist support for concurrent test runs
- ✅ **Retry Handling** - Configurable retry logic with exponential backoff
- ✅ **Reporting** - HTML and JSON reports with Allure integration
- ✅ **Environment Management** - Multi-environment support (dev, staging, production)
- ✅ **Scalable Structure** - Clear separation of concerns with modular design

## Project Structure

```
playwright_api_framework/
├── config/
│   ├── __init__.py
│   ├── settings.py              # Configuration management
│   └── environments.yaml         # Environment-specific configs
├── api/
│   ├── __init__.py
│   ├── base_client.py            # Base API client with retry logic
│   ├── posts_api.py              # Posts API object model
│   ├── users_api.py              # Users API object model
│   └── comments_api.py           # Comments API object model
├── utils/
│   ├── __init__.py
│   ├── logger.py                 # Custom logging
│   ├── assertions.py             # Custom assertions
│   ├── retry_handler.py          # Retry mechanism
│   └── decorators.py             # Useful decorators
├── data/
│   ├── __init__.py
│   ├── test_data.json            # Test data
│   └── fixtures.py               # Pytest fixtures
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_posts_api.py         # Posts API tests
│   ├── test_users_api.py         # Users API tests
│   └── test_comments_api.py      # Comments API tests
├── reports/                       # Test reports (generated)
├── logs/                          # Test logs (generated)
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
├── conftest.py                   # Global conftest
└── README.md                     # This file
```

## Installation

1. **Clone/create the project**
```bash
cd playwright_api_framework
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

## Configuration

### Environment Setup

Create `config/environments.yaml`:
```yaml
dev:
  base_url: "https://jsonplaceholder.typicode.com"
  timeout: 10000
  retries: 3
  
staging:
  base_url: "https://staging-api.example.com"
  timeout: 15000
  retries: 2
  
production:
  base_url: "https://api.example.com"
  timeout: 20000
  retries: 1
```

Set environment: `export TEST_ENV=dev`

## Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run with parallel execution (4 workers)
```bash
pytest tests/ -v -n 4
```

### Run specific test file
```bash
pytest tests/test_posts_api.py -v
```

### Run with HTML report
```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Run with Allure reporting
```bash
pytest tests/ -v --alluredir=reports/allure
allure serve reports/allure
```

### Run with detailed logging
```bash
pytest tests/ -v --log-cli-level=DEBUG
```

### Retry failed tests
```bash
pytest tests/ -v --reruns 3 --reruns-delay 2
```

## API Object Model Example

```python
from api.base_client import BaseAPIClient

class PostsAPI(BaseAPIClient):
    def get_posts(self) -> dict:
        return self.get("/posts")
    
    def get_post(self, post_id: int) -> dict:
        return self.get(f"/posts/{post_id}")
    
    def create_post(self, payload: dict) -> dict:
        return self.post("/posts", data=payload)

# Usage
posts_api = PostsAPI()
response = posts_api.get_posts()
```

## Best Practices

1. **Use fixtures** for API client initialization
2. **Parametrize tests** for multiple scenarios
3. **Assert both status and content** in API tests
4. **Use descriptive test names** following `test_<action>_<scenario>` pattern
5. **Log critical operations** for debugging
6. **Keep test data** in `data/` directory
7. **Use environment variables** for sensitive data

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run API Tests
  run: |
    pytest tests/ -v -n 4 --html=reports/report.html --alluredir=reports/allure
```

### Jenkins Example
```groovy
stage('Test') {
  steps {
    sh 'pytest tests/ -v -n 4 --junitxml=reports/junit.xml'
    junit 'reports/junit.xml'
  }
}
```

## Dependencies

- **Playwright** - Browser/API automation
- **Pytest** - Test framework
- **Pytest-xdist** - Parallel execution
- **Pytest-retry** - Retry mechanism
- **Pytest-html** - HTML reporting
- **Allure-pytest** - Allure reporting
- **PyYAML** - Configuration management
- **python-dotenv** - Environment variables

## Contributing

1. Follow the structure and naming conventions
2. Write descriptive test cases
3. Keep API classes in `api/` directory
4. Use utilities for common operations
5. Add logs for debugging

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests timeout | Increase `timeout` in config/environments.yaml |
| Retry not working | Ensure decorator is applied with correct params |
| Parallel tests fail | Check for shared state in fixtures |
| Reports not generated | Verify pytest plugins are installed |

---

**Created by:** Diksha More(Lead SDET)  
**Framework:** Playwright + Python  
**Last Updated:** 2026-05-24
