import time
from typing import Callable, TypeVar, Any
from functools import wraps
from utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T')

class RetryError(Exception):
    """Custom exception for retry failures"""
    pass


def retry(max_attempts: int = 3, delay: int = 1, backoff: float = 2.0):
    """
    Decorator for retrying functions with exponential backoff
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier for exponential delay
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            current_delay = delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.info(f"Attempt {attempt}/{max_attempts}: {func.__name__}")
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        logger.info(f"Success on attempt {attempt}")
                    return result
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt} failed: {str(e)}. "
                        f"Retrying in {current_delay}s..."
                    )
                    
                    if attempt < max_attempts:
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}"
                        )
            
            raise RetryError(
                f"Failed after {max_attempts} attempts: {str(last_exception)}"
            ) from last_exception
        
        return wrapper
    return decorator
