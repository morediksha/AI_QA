import pytest
from utils.assertions import APIAssertions
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.api
@pytest.mark.regression
class TestCommentsAPI:
    """Test suite for Comments API"""
    
    @pytest.mark.smoke
    def test_get_all_comments(self, comments_api):
        """Test: Get all comments"""
        response = comments_api.get_all_comments()
        
        APIAssertions.assert_response_is_list(response, min_length=1)
        APIAssertions.assert_response_contains_keys(
            response[0],
            ["postId", "id", "name", "email", "body"]
        )
        logger.info(f"Total comments: {len(response)}")
    
    @pytest.mark.smoke
    def test_get_specific_comment(self, comments_api):
        """Test: Get specific comment by ID"""
        comment_id = 1
        response = comments_api.get_comment(comment_id)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_contains_keys(
            response,
            ["postId", "id", "name", "email", "body"]
        )
        APIAssertions.assert_response_field(response, "id", comment_id)
    
    @pytest.mark.regression
    def test_get_comments_by_post(self, comments_api):
        """Test: Get all comments for a specific post"""
        post_id = 1
        response = comments_api.get_post_comments(post_id)
        
        APIAssertions.assert_response_is_list(response)
        if response:
            assert all(comment["postId"] == post_id for comment in response)
        logger.info(f"Post {post_id} has {len(response)} comments")
    
    @pytest.mark.regression
    def test_create_comment(self, fresh_comments_api):
        """Test: Create a new comment"""
        payload = {
            "postId": 1,
            "name": "Test Comment",
            "email": "test@example.com",
            "body": "This is a test comment"
        }
        response = fresh_comments_api.create_comment(payload)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_contains_keys(response, ["id", "postId", "name", "email", "body"])
        logger.info(f"Created comment with ID: {response.get('id')}")
    
    @pytest.mark.regression
    def test_update_comment(self, fresh_comments_api):
        """Test: Update existing comment"""
        comment_id = 1
        payload = {
            "id": comment_id,
            "postId": 1,
            "name": "Updated Comment",
            "email": "updated@example.com",
            "body": "Updated comment body"
        }
        response = fresh_comments_api.update_comment(comment_id, payload)
        
        APIAssertions.assert_response_not_empty(response)
        APIAssertions.assert_response_field(response, "name", "Updated Comment")
    
    @pytest.mark.regression
    def test_delete_comment(self, fresh_comments_api):
        """Test: Delete comment"""
        comment_id = 1
        response = fresh_comments_api.delete_comment(comment_id)
        
        APIAssertions.assert_response_type(response, dict)
        logger.info(f"Comment {comment_id} deleted successfully")
    
    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_get_comments_for_multiple_posts(self, comments_api, post_id):
        """Test: Get comments for multiple posts (parametrized)"""
        response = comments_api.get_post_comments(post_id)
        
        APIAssertions.assert_response_is_list(response)
        if response:
            assert all(comment["postId"] == post_id for comment in response)
        logger.info(f"Post {post_id} has {len(response)} comments")
    
    @pytest.mark.regression
    def test_comment_structure_validation(self, comments_api):
        """Test: Validate comment response structure"""
        response = comments_api.get_comment(1)
        
        required_fields = ["postId", "id", "name", "email", "body"]
        APIAssertions.assert_response_contains_keys(response, required_fields)
        
        # Validate field types
        assert isinstance(response["postId"], int)
        assert isinstance(response["id"], int)
        assert isinstance(response["name"], str)
        assert isinstance(response["email"], str)
        assert isinstance(response["body"], str)
