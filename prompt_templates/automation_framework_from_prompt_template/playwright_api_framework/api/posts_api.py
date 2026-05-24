from typing import List, Dict, Any, Optional
from api.base_client import BaseAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class PostsAPI(BaseAPIClient):
    """Posts API client for JSONPlaceholder"""
    
    POSTS_ENDPOINT = "/posts"
    
    def get_all_posts(self) -> List[Dict[str, Any]]:
        """Get all posts"""
        logger.info("Fetching all posts")
        return self.get(self.POSTS_ENDPOINT)
    
    def get_post(self, post_id: int) -> Dict[str, Any]:
        """Get specific post by ID"""
        logger.info(f"Fetching post with ID: {post_id}")
        return self.get(f"{self.POSTS_ENDPOINT}/{post_id}")
    
    def get_posts_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all posts by specific user"""
        logger.info(f"Fetching posts for user ID: {user_id}")
        return self.get(self.POSTS_ENDPOINT, params={"userId": user_id})
    
    def create_post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new post"""
        logger.info(f"Creating post with payload: {payload}")
        return self.post(self.POSTS_ENDPOINT, json=payload)
    
    def update_post(self, post_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing post"""
        logger.info(f"Updating post {post_id} with payload: {payload}")
        return self.put(f"{self.POSTS_ENDPOINT}/{post_id}", json=payload)
    
    def partial_update_post(self, post_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Partially update post"""
        logger.info(f"Partially updating post {post_id} with payload: {payload}")
        return self.patch(f"{self.POSTS_ENDPOINT}/{post_id}", json=payload)
    
    def delete_post(self, post_id: int) -> Dict[str, Any]:
        """Delete post"""
        logger.info(f"Deleting post {post_id}")
        return self.delete(f"{self.POSTS_ENDPOINT}/{post_id}")
