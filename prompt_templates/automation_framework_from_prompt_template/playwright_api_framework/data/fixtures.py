import json
from pathlib import Path

# Test data directory
DATA_DIR = Path(__file__).parent

# Sample test data
SAMPLE_POST = {
    "title": "Test Post Title",
    "body": "This is a test post body",
    "userId": 1
}

SAMPLE_USER = {
    "name": "John Doe",
    "email": "john@example.com",
    "username": "johndoe",
    "phone": "1-770-736-8031",
    "website": "https://example.com"
}

SAMPLE_COMMENT = {
    "postId": 1,
    "name": "Test Comment",
    "email": "test@example.com",
    "body": "This is a test comment"
}

# Load test data from JSON if available
def load_test_data(filename: str) -> dict:
    """Load test data from JSON file"""
    filepath = DATA_DIR / f"{filename}.json"
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}
