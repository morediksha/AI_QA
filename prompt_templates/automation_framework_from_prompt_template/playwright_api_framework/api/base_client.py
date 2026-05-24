import requests
from typing import Optional, Dict, Any
from config.settings import settings
from utils.logger import get_logger
from utils.retry_handler import retry

logger = get_logger(__name__)


class BaseAPIClient:
    """Base API client with retry logic and common methods"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.base_url
        self.timeout = settings.timeout / 1000  # Convert to seconds
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        return f"{self.base_url}{endpoint}"
    
    @retry(max_attempts=3, delay=1, backoff=2.0)
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request with retry"""
        url = self._build_url(endpoint)
        logger.info(f"GET {url}")
        
        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        logger.info(f"Response: {response.status_code}")
        return response.json()
    
    @retry(max_attempts=3, delay=1, backoff=2.0)
    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """POST request with retry"""
        url = self._build_url(endpoint)
        logger.info(f"POST {url}")
        
        _headers = {**self.session.headers, **(headers or {})}
        response = self.session.post(
            url,
            data=data,
            json=json,
            headers=_headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        logger.info(f"Response: {response.status_code}")
        return response.json() if response.content else {}
    
    @retry(max_attempts=3, delay=1, backoff=2.0)
    def put(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """PUT request with retry"""
        url = self._build_url(endpoint)
        logger.info(f"PUT {url}")
        
        _headers = {**self.session.headers, **(headers or {})}
        response = self.session.put(
            url,
            data=data,
            json=json,
            headers=_headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        logger.info(f"Response: {response.status_code}")
        return response.json() if response.content else {}
    
    @retry(max_attempts=3, delay=1, backoff=2.0)
    def patch(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """PATCH request with retry"""
        url = self._build_url(endpoint)
        logger.info(f"PATCH {url}")
        
        _headers = {**self.session.headers, **(headers or {})}
        response = self.session.patch(
            url,
            data=data,
            json=json,
            headers=_headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        logger.info(f"Response: {response.status_code}")
        return response.json() if response.content else {}
    
    @retry(max_attempts=3, delay=1, backoff=2.0)
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """DELETE request with retry"""
        url = self._build_url(endpoint)
        logger.info(f"DELETE {url}")
        
        _headers = {**self.session.headers, **(headers or {})}
        response = self.session.delete(
            url,
            headers=_headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        logger.info(f"Response: {response.status_code}")
        return response.json() if response.content else {}
    
    def close(self):
        """Close session"""
        self.session.close()
        logger.info("Session closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
