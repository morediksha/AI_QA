# Best Practices for API Automation

## 1. Test Design

### ✅ DO: Use Clear, Descriptive Test Names
```python
# Good
def test_get_post_returns_correct_id(self):
def test_create_post_with_valid_payload_succeeds(self):
def test_get_nonexistent_post_returns_404(self):

# Avoid
def test_post(self):
def test_create(self):
def test_get(self):
```

### ✅ DO: Follow AAA Pattern (Arrange, Act, Assert)
```python
def test_create_post(self, posts_api):
    # Arrange
    payload = {
        "title": "Test Post",
        "body": "Test Body",
        "userId": 1
    }
    
    # Act
    response = posts_api.create_post(payload)
    
    # Assert
    APIAssertions.assert_response_contains_keys(response, ["id", "title"])
```

### ✅ DO: Test Edge Cases
```python
@pytest.mark.parametrize("user_id", [1, 999, -1, 0, "invalid"])
def test_get_user_edge_cases(self, users_api, user_id):
    # Tests boundary conditions
```

### ❌ DON'T: Create Test Dependencies
```python
# Bad - tests depend on execution order
def test_1_create_user(self):
    ...

def test_2_get_user(self):  # Depends on test_1
    ...

# Good - tests are independent
@pytest.fixture
def user(self):
    return create_test_user()

def test_get_created_user(self, user):
    ...
```

## 2. Assertions

### ✅ DO: Use Specific Assertions
```python
# Good - Clear what's being tested
APIAssertions.assert_status_code(response, 200)
APIAssertions.assert_response_field(response, "userId", 1)

# Avoid - Generic assertions
assert response is not None
assert "id" in response
```

### ✅ DO: Assert Both Status and Content
```python
def test_get_post(self, posts_api):
    response = posts_api.get_post(1)
    
    # Check status was successful
    APIAssertions.assert_response_not_empty(response)
    
    # Check content is correct
    APIAssertions.assert_response_contains_keys(response, ["id", "title"])
    APIAssertions.assert_response_field(response, "id", 1)
```

### ✅ DO: Provide Context in Assertions
```python
# Good
assert user["age"] >= 18, f"User {user['id']} is underage"

# Better
APIAssertions.assert_response_field(
    user,
    "age",
    expected_value=18,
    message=f"User {user['id']} must be 18+"
)
```

## 3. API Object Model

### ✅ DO: Encapsulate Endpoints
```python
class PostsAPI(BaseAPIClient):
    # Don't expose raw endpoints
    # Instead, expose business operations
    
    def get_all_posts(self) -> List[Dict]:
        """Get all posts"""
        return self.get("/posts")
    
    def get_posts_by_user(self, user_id: int) -> List[Dict]:
        """Get user's posts - encapsulates filtering logic"""
        return self.get("/posts", params={"userId": user_id})
```

### ✅ DO: Document API Methods
```python
def create_post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new post.
    
    Args:
        payload: Dictionary with keys: userId, title, body
        
    Returns:
        Response dict with id, title, body, userId
        
    Raises:
        requests.HTTPError: If creation fails
    """
    return self.post("/posts", json=payload)
```

### ❌ DON'T: Expose Raw Endpoints
```python
# Bad - tests know too much about API structure
response = requests.get(f"{base_url}/posts/{post_id}")

# Good - API object hides implementation
response = posts_api.get_post(post_id)
```

## 4. Test Data Management

### ✅ DO: Use Centralized Test Data
```python
# data/fixtures.py
SAMPLE_POST = {
    "title": "Test Post",
    "body": "Test Body",
    "userId": 1
}

# test_posts_api.py
from data.fixtures import SAMPLE_POST

def test_create_post(self, posts_api):
    response = posts_api.create_post(SAMPLE_POST)
```

### ✅ DO: Use Parametrization for Multiple Scenarios
```python
@pytest.mark.parametrize("user_id,expected_count", [
    (1, 10),
    (2, 8),
    (3, 5),
])
def test_user_post_counts(self, users_api, user_id, expected_count):
    posts = users_api.get_user_posts(user_id)
    assert len(posts) == expected_count
```

### ❌ DON'T: Hardcode Test Data in Tests
```python
# Bad
def test_create_post(self, posts_api):
    response = posts_api.create_post({
        "title": "Test",
        "body": "Body",
        "userId": 1
    })

# Good - Extracted to data/fixtures.py
def test_create_post(self, posts_api):
    response = posts_api.create_post(SAMPLE_POST)
```

## 5. Error Handling & Debugging

### ✅ DO: Use Proper Logging
```python
from utils.logger import get_logger

logger = get_logger(__name__)

def test_complex_scenario(self, api):
    logger.info("Starting complex test scenario")
    
    response = api.get_resource(1)
    logger.debug(f"Got response: {response}")
    
    assert response["status"] == "active", "Resource should be active"
    logger.info("Test passed")
```

### ✅ DO: Handle API Errors Gracefully
```python
def test_api_error_handling(self, posts_api):
    try:
        response = posts_api.get_post(99999)  # Non-existent
        assert False, "Should have raised error"
    except requests.HTTPError as e:
        logger.info(f"Expected error: {e}")
        assert e.response.status_code == 404
```

### ✅ DO: Use Descriptive Error Messages
```python
assert response["userId"] in [1, 2, 3], \
    f"User {response['userId']} not in allowed list"
```

## 6. Fixtures & Setup/Teardown

### ✅ DO: Use Appropriate Fixture Scopes
```python
@pytest.fixture(scope="session")
def posts_api():
    """Created once per test session - efficient"""
    client = PostsAPI()
    yield client
    client.close()

@pytest.fixture(scope="function")
def fresh_posts_api():
    """Created per test - clean state"""
    client = PostsAPI()
    yield client
    client.close()
```

### ✅ DO: Cleanup Resources
```python
@pytest.fixture
def test_user(users_api):
    # Setup
    user = users_api.create_user(SAMPLE_USER)
    yield user
    
    # Cleanup
    users_api.delete_user(user["id"])
    logger.info(f"Deleted test user {user['id']}")
```

### ❌ DON'T: Mix Setup and Test Logic
```python
# Bad
def test_get_user(self, users_api):
    # Setup mixed with test
    user = users_api.create_user(SAMPLE_USER)
    
    response = users_api.get_user(user["id"])
    assert response["id"] == user["id"]

# Good - Use fixtures for setup
@pytest.fixture
def created_user(users_api):
    return users_api.create_user(SAMPLE_USER)

def test_get_user(self, created_user):
    # Test logic only
    response = users_api.get_user(created_user["id"])
    assert response["id"] == created_user["id"]
```

## 7. Test Isolation

### ✅ DO: Keep Tests Independent
```python
# Each test should work alone
def test_create_post(self, posts_api):
    response = posts_api.create_post(SAMPLE_POST)
    assert "id" in response

def test_get_post(self, posts_api):
    # Doesn't depend on previous test
    response = posts_api.get_post(1)
    assert response["id"] == 1
```

### ✅ DO: Clean Up After Tests
```python
@pytest.fixture
def temporary_post(posts_api):
    post = posts_api.create_post(SAMPLE_POST)
    yield post
    
    # Always cleanup, even if test fails
    posts_api.delete_post(post["id"])
```

### ❌ DON'T: Share State Between Tests
```python
# Bad - shared state
class TestPosts:
    posts = []  # Shared across tests!
    
    def test_create(self):
        self.posts.append(...)
```

## 8. Parametrization

### ✅ DO: Use Parametrization for Similar Tests
```python
@pytest.mark.parametrize("post_id,expected_title", [
    (1, "Test Post 1"),
    (2, "Test Post 2"),
    (3, "Test Post 3"),
])
def test_get_posts(self, posts_api, post_id, expected_title):
    response = posts_api.get_post(post_id)
    assert response["title"] == expected_title
```

### ✅ DO: Use Indirect Parametrization for Complex Setup
```python
@pytest.fixture
def user(request):
    user_id = request.param
    return users_api.get_user(user_id)

@pytest.mark.parametrize("user", [1, 2, 3], indirect=True)
def test_user_properties(self, user):
    assert user["id"] is not None
```

## 9. Markers & Organization

### ✅ DO: Use Markers for Test Organization
```python
@pytest.mark.smoke
@pytest.mark.api
def test_critical_endpoint(self):
    """Runs in quick smoke test suite"""

@pytest.mark.regression
@pytest.mark.api
def test_edge_case(self):
    """Runs in full regression"""

@pytest.mark.slow
def test_performance(self):
    """Runs separately"""
```

## 10. CI/CD Integration

### ✅ DO: Structure Tests for CI/CD
```bash
# Fast smoke tests for every commit
pytest tests/ -m smoke -v

# Full regression on schedule
pytest tests/ -v -n 4

# Specific environment testing
pytest tests/ -v --override-ini="TEST_ENV=staging"
```

### ✅ DO: Generate Reports for CI/CD
```bash
pytest tests/ \
  -v \
  --html=reports/report.html \
  --junitxml=reports/junit.xml \
  --alluredir=reports/allure
```

## 11. Retry Strategy

### ✅ DO: Use Retry for Flaky Tests
```python
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_sometimes_flaky_endpoint(self, api):
    # Reruns up to 3 times with 2s delay
    response = api.get_resource()
```

### ✅ DO: Configure Retry in Framework
```python
# config/settings.py
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1
RETRY_BACKOFF = 2.0

# All API calls use these defaults
```

## 12. Code Organization

### ✅ DO: Follow Clear Directory Structure
```
api/              # API Objects
  posts_api.py
  users_api.py
utils/            # Utilities
  logger.py
  assertions.py
tests/            # Test Cases
  test_posts_api.py
  test_users_api.py
data/             # Test Data
  fixtures.py
  test_data.json
```

### ✅ DO: Keep Related Code Together
```python
# Bad - scattered
def test_1(): ...
def helper_1(): ...
def test_2(): ...
def helper_2(): ...

# Good - organized
def helper_1(): ...
def helper_2(): ...
def test_1(): ...
def test_2(): ...
```

## 13. Performance

### ✅ DO: Optimize Test Execution
```bash
# Profile slow tests
pytest tests/ --durations=10

# Run fast tests in parallel
pytest tests/ -m "not slow" -n 4

# Skip UI tests if testing API only
pytest tests/ -k "not ui"
```

### ✅ DO: Reuse API Clients
```python
@pytest.fixture(scope="session")
def posts_api():
    """Shared across all tests"""
    return PostsAPI()
```

---

**Last Updated:** 2026-05-24  
**Framework:** Playwright + Python
