import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.posts_api import PostsAPI
from api.users_api import UsersAPI
from api.comments_api import CommentsAPI
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def posts_api():
    """Create posts API client for entire session"""
    client = PostsAPI()
    logger.info("Posts API client initialized")
    yield client
    client.close()


@pytest.fixture(scope="session")
def users_api():
    """Create users API client for entire session"""
    client = UsersAPI()
    logger.info("Users API client initialized")
    yield client
    client.close()


@pytest.fixture(scope="session")
def comments_api():
    """Create comments API client for entire session"""
    client = CommentsAPI()
    logger.info("Comments API client initialized")
    yield client
    client.close()


@pytest.fixture(scope="function")
def fresh_posts_api():
    """Create fresh posts API client for each test"""
    client = PostsAPI()
    yield client
    client.close()


@pytest.fixture(scope="function")
def fresh_users_api():
    """Create fresh users API client for each test"""
    client = UsersAPI()
    yield client
    client.close()


@pytest.fixture(scope="function")
def fresh_comments_api():
    """Create fresh comments API client for each test"""
    client = CommentsAPI()
    yield client
    client.close()


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Automatically log test start and end"""
    logger.info(f"{'='*60}")
    logger.info(f"Starting test: {request.node.name}")
    logger.info(f"{'='*60}")
    yield
    logger.info(f"Completed test: {request.node.name}")
