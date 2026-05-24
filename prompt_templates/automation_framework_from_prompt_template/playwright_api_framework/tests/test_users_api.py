import pytest
from utils.assertions import APIAssertions
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.api
@pytest.mark.regression
class TestUsersAPI:
    """Test suite for Users API"""
    
    @pytest.mark.smoke
    def test_get_all_users(self, users_api):
        """Test: Get all users"""
        response = users_api.get_all_users()
        
        APIAssertions.assert_response_is_list(response, min_length=1)
        APIAssertions.assert_response_contains_keys(
            response[0],
            ["id", "name", "username", "email"]
        )
        logger.info(f"Total users: {len(response)}")
    
    @pytest.mark.smoke
    def test_get_specific_user(self, users_api):
        """Test: Get specific user by ID"""
        user_id = 1
        response = users_api.get_user(user_id)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_contains_keys(
            response,
            ["id", "name", "username", "email"]
        )
        APIAssertions.assert_response_field(response, "id", user_id)
    
    @pytest.mark.regression
    def test_create_user(self, fresh_users_api):
        """Test: Create a new user"""
        payload = {
            "name": "Test User",
            "email": "testuser@example.com",
            "username": "testuser",
            "phone": "123-456-7890",
            "website": "https://testuser.com"
        }
        response = fresh_users_api.create_user(payload)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_contains_keys(response, ["id", "name", "email"])
        logger.info(f"Created user with ID: {response.get('id')}")
    
    @pytest.mark.regression
    def test_update_user(self, fresh_users_api):
        """Test: Update existing user"""
        user_id = 1
        payload = {
            "id": user_id,
            "name": "Updated User Name",
            "email": "updated@example.com",
            "username": "updated_user"
        }
        response = fresh_users_api.update_user(user_id, payload)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_field(response, "name", "Updated User Name")
    
    @pytest.mark.regression
    def test_delete_user(self, fresh_users_api):
        """Test: Delete user"""
        user_id = 1
        response = fresh_users_api.delete_user(user_id)
        
        APIAssertions.assert_response_type(response, dict)
        logger.info(f"User {user_id} deleted successfully")
    
    @pytest.mark.regression
    def test_get_user_posts(self, users_api):
        """Test: Get all posts by user"""
        user_id = 1
        response = users_api.get_user_posts(user_id)
        
        APIAssertions.assert_response_is_list(response)
        if response:
            assert all(post["userId"] == user_id for post in response)
        logger.info(f"User {user_id} has {len(response)} posts")
    
    @pytest.mark.regression
    def test_get_user_albums(self, users_api):
        """Test: Get all albums by user"""
        user_id = 1
        response = users_api.get_user_albums(user_id)
        
        APIAssertions.assert_response_is_list(response)
        if response:
            assert all(album["userId"] == user_id for album in response)
        logger.info(f"User {user_id} has {len(response)} albums")
    
    @pytest.mark.regression
    def test_get_user_todos(self, users_api):
        """Test: Get all todos by user"""
        user_id = 1
        response = users_api.get_user_todos(user_id)
        
        APIAssertions.assert_response_is_list(response)
        if response:
            assert all(todo["userId"] == user_id for todo in response)
        logger.info(f"User {user_id} has {len(response)} todos")
    
    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    def test_get_multiple_users(self, users_api, user_id):
        """Test: Verify multiple users exist (parametrized)"""
        response = users_api.get_user(user_id)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_field(response, "id", user_id)
        logger.info(f"Verified user {user_id}: {response.get('name')}")
    
    @pytest.mark.regression
    def test_user_structure_validation(self, users_api):
        """Test: Validate user response structure"""
        response = users_api.get_user(1)
        
        required_fields = ["id", "name", "username", "email", "address", "phone", "website", "company"]
        APIAssertions.assert_response_contains_keys(response, required_fields)
        
        # Validate field types
        assert isinstance(response["id"], int)
        assert isinstance(response["name"], str)
        assert isinstance(response["email"], str)
        assert isinstance(response["address"], dict)
