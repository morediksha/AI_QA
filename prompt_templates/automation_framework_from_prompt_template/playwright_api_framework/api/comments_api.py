from typing import List, Dict, Any, Optional
from api.base_client import BaseAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class CommentsAPI(BaseAPIClient):
    """Comments API client for JSONPlaceholder"""
    
    COMMENTS_ENDPOINT = "/comments"
    
    def get_all_comments(self) -> List[Dict[str, Any]]:
        """Get all comments"""
        logger.info("Fetching all comments")
        return self.get(self.COMMENTS_ENDPOINT)
    
    def get_comment(self, comment_id: int) -> Dict[str, Any]:
        """Get specific comment by ID"""
        logger.info(f"Fetching comment with ID: {comment_id}")
        return self.get(f"{self.COMMENTS_ENDPOINT}/{comment_id}")
    
    def get_post_comments(self, post_id: int) -> List[Dict[str, Any]]:
        """Get all comments for specific post"""
        logger.info(f"Fetching comments for post ID: {post_id}")
        return self.get(self.COMMENTS_ENDPOINT, params={"postId": post_id})
    
    def create_comment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new comment"""
        logger.info(f"Creating comment with payload: {payload}")
        return self.post(self.COMMENTS_ENDPOINT, json=payload)
    
    def update_comment(self, comment_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing comment"""
        logger.info(f"Updating comment {comment_id} with payload: {payload}")
        return self.put(f"{self.COMMENTS_ENDPOINT}/{comment_id}", json=payload)
    
    def delete_comment(self, comment_id: int) -> Dict[str, Any]:
        """Delete comment"""
        logger.info(f"Deleting comment {comment_id}")
        return self.delete(f"{self.COMMENTS_ENDPOINT}/{comment_id}")
