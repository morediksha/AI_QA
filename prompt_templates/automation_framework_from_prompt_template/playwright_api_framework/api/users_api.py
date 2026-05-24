from typing import List, Dict, Any, Optional
from api.base_client import BaseAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class UsersAPI(BaseAPIClient):
    """Users API client for JSONPlaceholder"""
    
    USERS_ENDPOINT = "/users"
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        logger.info("Fetching all users")
        return self.get(self.USERS_ENDPOINT)
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get specific user by ID"""
        logger.info(f"Fetching user with ID: {user_id}")
        return self.get(f"{self.USERS_ENDPOINT}/{user_id}")
    
    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        logger.info(f"Creating user with payload: {payload}")
        return self.post(self.USERS_ENDPOINT, json=payload)
    
    def update_user(self, user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing user"""
        logger.info(f"Updating user {user_id} with payload: {payload}")
        return self.put(f"{self.USERS_ENDPOINT}/{user_id}", json=payload)
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete user"""
        logger.info(f"Deleting user {user_id}")
        return self.delete(f"{self.USERS_ENDPOINT}/{user_id}")
    
    def get_user_posts(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all posts by specific user"""
        logger.info(f"Fetching posts for user {user_id}")
        return self.get(f"{self.USERS_ENDPOINT}/{user_id}/posts")
    
    def get_user_albums(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all albums by specific user"""
        logger.info(f"Fetching albums for user {user_id}")
        return self.get(f"{self.USERS_ENDPOINT}/{user_id}/albums")
    
    def get_user_todos(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all todos by specific user"""
        logger.info(f"Fetching todos for user {user_id}")
        return self.get(f"{self.USERS_ENDPOINT}/{user_id}/todos")
