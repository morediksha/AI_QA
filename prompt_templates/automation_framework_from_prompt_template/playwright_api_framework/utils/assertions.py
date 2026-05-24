from typing import Any
import pytest
from utils.logger import get_logger

logger = get_logger(__name__)


class APIAssertions:
    """Custom assertions for API testing"""
    
    @staticmethod
    def assert_status_code(
        status_code: int,
        expected: int,
        message: str = ""
    ) -> None:
        """Assert response status code"""
        assert status_code == expected, (
            f"Expected status {expected}, got {status_code}. {message}"
        )
        logger.info(f"✓ Status code assertion passed: {status_code}")
    
    @staticmethod
    def assert_response_contains_keys(
        response: dict,
        required_keys: list,
        message: str = ""
    ) -> None:
        """Assert response contains required keys"""
        missing_keys = [key for key in required_keys if key not in response]
        assert not missing_keys, (
            f"Missing keys in response: {missing_keys}. {message}"
        )
        logger.info(f"✓ Response contains all required keys: {required_keys}")
    
    @staticmethod
    def assert_response_field(
        response: dict,
        field: str,
        expected_value: Any,
        message: str = ""
    ) -> None:
        """Assert specific field in response has expected value"""
        actual = response.get(field)
        assert actual == expected_value, (
            f"Expected {field}={expected_value}, got {actual}. {message}"
        )
        logger.info(f"✓ Field assertion passed: {field}={expected_value}")
    
    @staticmethod
    def assert_response_not_empty(
        response: dict,
        message: str = ""
    ) -> None:
        """Assert response is not empty"""
        assert response, f"Response is empty. {message}"
        logger.info("✓ Response is not empty")
    
    @staticmethod
    def assert_response_is_list(
        response: Any,
        min_length: int = 0,
        message: str = ""
    ) -> None:
        """Assert response is a list with minimum length"""
        assert isinstance(response, list), (
            f"Response is not a list. {message}"
        )
        assert len(response) >= min_length, (
            f"Response list has {len(response)} items, expected at least {min_length}. {message}"
        )
        logger.info(f"✓ Response is a list with {len(response)} items")
    
    @staticmethod
    def assert_response_type(
        response: Any,
        expected_type: type,
        message: str = ""
    ) -> None:
        """Assert response is of expected type"""
        assert isinstance(response, expected_type), (
            f"Expected {expected_type.__name__}, got {type(response).__name__}. {message}"
        )
        logger.info(f"✓ Response type assertion passed: {expected_type.__name__}")
