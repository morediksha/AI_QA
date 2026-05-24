import pytest
from utils.assertions import APIAssertions
from data.fixtures import SAMPLE_POST
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.api
@pytest.mark.regression
class TestPostsAPI:
    """Test suite for Posts API"""
    
    @pytest.mark.smoke
    def test_get_all_posts(self, posts_api):
        """Test: Get all posts"""
        response = posts_api.get_all_posts()
        
        APIAssertions.assert_response_is_list(response, min_length=1)
        APIAssertions.assert_response_contains_keys(response[0], ["id", "userId", "title", "body"])
        logger.info(f"Total posts: {len(response)}")
    
    @pytest.mark.smoke
    def test_get_specific_post(self, posts_api):
        """Test: Get specific post by ID"""
        post_id = 1
        response = posts_api.get_post(post_id)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_contains_keys(response, ["id", "userId", "title", "body"])
        APIAssertions.assert_response_field(response, "id", post_id)
    
    @pytest.mark.regression
    def test_get_posts_by_user(self, posts_api):
        """Test: Get posts filtered by user"""
        user_id = 1
        response = posts_api.get_posts_by_user(user_id)
        
        APIAssertions.assert_response_is_list(response)
        assert all(post["userId"] == user_id for post in response), \
            "Not all posts belong to the specified user"
        logger.info(f"Posts for user {user_id}: {len(response)}")
    
    @pytest.mark.regression
    def test_create_post(self, fresh_posts_api):
        """Test: Create a new post"""
        payload = {
            "title": "New Test Post",
            "body": "This is a test post body",
            "userId": 1
        }
        response = fresh_posts_api.create_post(payload)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_contains_keys(response, ["id", "title", "body", "userId"])
        logger.info(f"Created post with ID: {response.get('id')}")
    
    @pytest.mark.regression
    def test_update_post(self, fresh_posts_api):
        """Test: Update existing post"""
        post_id = 1
        payload = {
            "id": post_id,
            "title": "Updated Title",
            "body": "Updated body",
            "userId": 1
        }
        response = fresh_posts_api.update_post(post_id, payload)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_field(response, "title", "Updated Title")
    
    @pytest.mark.regression
    def test_partial_update_post(self, fresh_posts_api):
        """Test: Partially update post"""
        post_id = 1
        payload = {"title": "Partially Updated Title"}
        response = fresh_posts_api.partial_update_post(post_id, payload)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_contains_keys(response, ["id", "title"])
    
    @pytest.mark.regression
    def test_delete_post(self, fresh_posts_api):
        """Test: Delete post"""
        post_id = 1
        response = fresh_posts_api.delete_post(post_id)
        
        # JSONPlaceholder returns empty object on delete
        APIAssertions.assert_response_type(response, dict)
        logger.info(f"Post {post_id} deleted successfully")
    
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_posts_by_multiple_users(self, posts_api, user_id):
        """Test: Get posts for multiple users (parametrized)"""
        response = posts_api.get_posts_by_user(user_id)
        
        APIAssertions.assert_response_is_list(response)
        if response:
            assert all(post["userId"] == user_id for post in response)
        logger.info(f"Verified posts for user {user_id}")
    
    @pytest.mark.regression
    def test_post_structure_validation(self, posts_api):
        """Test: Validate post response structure"""
        response = posts_api.get_post(1)
        
        required_fields = ["userId", "id", "title", "body"]
        APIAssertions.assert_response_contains_keys(response, required_fields)
        
        # Validate field types
        assert isinstance(response["id"], int)
        assert isinstance(response["userId"], int)
        assert isinstance(response["title"], str)
        assert isinstance(response["body"], str)
