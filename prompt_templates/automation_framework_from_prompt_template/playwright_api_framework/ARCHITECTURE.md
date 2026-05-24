# Framework Architecture & Design

## Overview

The Playwright API Automation Framework is built on **layered architecture** following best practices for test automation, maintainability, and scalability.

```
┌─────────────────────────────────────────┐
│         Tests Layer                     │
│  (test_*.py - Test Cases)              │
├─────────────────────────────────────────┤
│         API Object Model Layer          │
│  (posts_api.py, users_api.py, etc)     │
├─────────────────────────────────────────┤
│         Base API Client Layer           │
│  (base_client.py - HTTP methods)       │
├─────────────────────────────────────────┤
│         Utilities Layer                 │
│  (logger, assertions, retry, etc)      │
├─────────────────────────────────────────┤
│         Configuration Layer             │
│  (settings, environments)               │
├─────────────────────────────────────────┤
│         External APIs                   │
│  (RESTful APIs being tested)            │
└─────────────────────────────────────────┘
```

## Architecture Components

### 1. **Configuration Layer** (`config/`)
- **Purpose:** Centralized configuration management
- **Files:**
  - `settings.py` - Application settings and environment management
  - `environments.yaml` - Environment-specific configurations (dev, staging, prod)
  - `.env.example` - Environment variable template

**Key Concepts:**
```python
from config.settings import settings
base_url = settings.base_url  # Dynamically loaded from environment
timeout = settings.timeout
max_retries = settings.max_retries
```

### 2. **Base API Client Layer** (`api/base_client.py`)
- **Purpose:** Core HTTP communication with retry logic
- **Responsibilities:**
  - HTTP request handling (GET, POST, PUT, PATCH, DELETE)
  - Automatic retry with exponential backoff
  - Session management
  - URL building

**Design Pattern:** Base class pattern with decorator-based retry logic

```python
class BaseAPIClient:
    @retry(max_attempts=3, delay=1, backoff=2.0)
    def get(self, endpoint: str) -> Dict:
        # HTTP GET with automatic retry
```

### 3. **API Object Model Layer** (`api/`)
- **Purpose:** Abstracts API endpoints into reusable, documented interfaces
- **Files:**
  - `posts_api.py` - Posts API operations
  - `users_api.py` - Users API operations
  - `comments_api.py` - Comments API operations

**Design Pattern:** Page Object Model adapted for APIs

**Example:**
```python
class PostsAPI(BaseAPIClient):
    def get_posts(self) -> List[Dict]:
        # Encapsulates endpoint logic
        
    def create_post(self, payload: Dict) -> Dict:
        # Encapsulates POST operation
```

**Benefits:**
- Single source of truth for API endpoints
- Easy to update when API changes
- Reusable across multiple tests
- Better error messages

### 4. **Utilities Layer** (`utils/`)
- **Logger** (`logger.py`) - Custom logging with file and console output
- **Assertions** (`assertions.py`) - API-specific assertion methods
- **Retry Handler** (`retry_handler.py`) - Decorator-based retry mechanism

**Design Patterns:**
- Decorator pattern (for retry logic)
- Singleton pattern (for logger)
- Custom assertion helper methods

### 5. **Test Layer** (`tests/`)
- **Purpose:** Test cases and test fixtures
- **Files:**
  - `conftest.py` - Pytest configuration and fixtures
  - `test_posts_api.py` - Posts API test suite
  - `test_users_api.py` - Users API test suite
  - `test_comments_api.py` - Comments API test suite

**Test Structure:**
```
@pytest.mark.api              # Test category
@pytest.mark.regression       # Test type
class TestPostsAPI:           # Test class
    @pytest.mark.smoke        # Test priority
    def test_get_all_posts(): # Test method
```

## Design Patterns Used

### 1. **Page Object Model (adapted for APIs)**
```
API Object → Encapsulates endpoints
         ↓
         Exposes clean methods
         ↓
         Test uses methods, not endpoints
```

### 2. **Decorator Pattern (Retry Logic)**
```python
@retry(max_attempts=3, delay=1, backoff=2.0)
def get(self, endpoint: str):
    # Automatically retried on failure
```

### 3. **Fixture Pattern (Setup/Teardown)**
```python
@pytest.fixture
def posts_api():
    client = PostsAPI()
    yield client
    client.close()  # Cleanup
```

### 4. **Factory Pattern (Fixture Creation)**
```python
@pytest.fixture(scope="session")
def posts_api():  # Session-scoped - created once
    ...

@pytest.fixture(scope="function")
def fresh_posts_api():  # Function-scoped - created per test
    ...
```

## Data Flow

### Test Execution Flow
```
Test Method
    ↓
Fixture (API Client) ← Configuration loaded
    ↓
API Object (posts_api.get_post)
    ↓
Base Client (self.get)
    ↓
Retry Decorator (checks for failure)
    ↓
HTTP Request (requests library)
    ↓
Response
    ↓
Logger (logs result)
    ↓
Assertions (validates response)
    ↓
Test Result
```

## Parallel Execution Architecture

The framework uses `pytest-xdist` for parallel execution:

```
Tests Distribution
├── Worker 1 → test_posts_api.py (1-3)
├── Worker 2 → test_posts_api.py (4-6)
├── Worker 3 → test_users_api.py (1-3)
└── Worker 4 → test_users_api.py (4-6)
```

**Isolation Strategy:**
- Each worker has independent API client instance
- No shared state between workers
- Session-scoped fixtures initialized once per session
- Function-scoped fixtures created per test

## Error Handling Strategy

```
HTTP Request
    ↓
Status Check
    ├─ Success (200-299) → Return response
    ├─ Retry-able error (timeout, 429, 5xx) → Retry with backoff
    └─ Non-retry-able error (400, 401, 403) → Fail immediately
```

## Logging Architecture

```
Log Entry
    ├─ Console Handler → Terminal output
    ├─ File Handler → logs/*.log
    └─ Both use same formatter with timestamps
```

## Configuration Resolution

```
1. Check .env file
    ↓
2. If not found, use .env.example defaults
    ↓
3. If not found, use built-in defaults
    ↓
4. Override with environment variables
```

## Extensibility Points

### Adding New API
1. Create new file: `api/new_api.py`
2. Extend `BaseAPIClient`
3. Add test file: `tests/test_new_api.py`

### Adding New Assertion
```python
# In utils/assertions.py
@staticmethod
def assert_custom_condition(response, condition):
    assert condition, f"Custom assertion failed"
```

### Custom Retry Logic
```python
@retry(max_attempts=5, delay=2, backoff=1.5)
def custom_method(self):
    # Overrides default retry behavior
```

### Environment-Specific Tests
```python
@pytest.mark.skipif(
    settings.TEST_ENV != "staging",
    reason="Only runs in staging"
)
def test_staging_only():
    ...
```

## Performance Considerations

### Optimization Strategies
1. **Session-scoped fixtures** - Reuse API clients across tests
2. **Parallel execution** - Use 4-8 workers based on system
3. **Retry backoff** - Exponential backoff reduces API overload
4. **Connection pooling** - `requests.Session` reuses connections

### Metrics Collection
```bash
# Profile test execution
pytest tests/ -v --durations=10

# Shows slowest 10 tests
```

## Security Considerations

1. **Secrets Management**
   - Use `.env` file (not version controlled)
   - Never commit sensitive data
   - Use environment variables in CI/CD

2. **API Key Handling**
   ```python
   api_key = os.getenv("API_KEY")
   headers = {"Authorization": f"Bearer {api_key}"}
   ```

3. **HTTPS Only**
   ```python
   base_url = "https://api.example.com"  # Always HTTPS
   ```

## Maintenance Guidelines

### When to Update
- API endpoint changes → Update API object class
- New test scenarios → Add test method
- Shared utilities → Add to utils/ directory

### When to Extend
- New API endpoints → Create new API object class
- Common test patterns → Create utility function
- Environment variations → Add to environments.yaml

---

**Last Updated:** 2026-05-24  
**Framework:** Playwright + Python
