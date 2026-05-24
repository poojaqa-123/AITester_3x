"""
REST API Base Test Class with fluent API and REST Assured style methods
"""
import requests
import json
import logging
from typing import Any, Dict, List, Optional
from config import BASE_URL, DEFAULT_TIMEOUT, DEFAULT_HEADERS

# Setup logging
logger = logging.getLogger(__name__)


class RestApiClient:
    """
    REST API Client with fluent interface (REST Assured style)
    Supports request building, response handling, and assertions
    """
    
    def __init__(self, base_url: str = BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        """Initialize REST API client"""
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.response = None
        self._request_log = []
    
    # ==================== REQUEST BUILDING ====================
    
    def given(self):
        """Start a given-when-then style request (REST Assured pattern)"""
        return self
    
    def when(self):
        """Execute when clause (REST Assured pattern)"""
        return self
    
    def then(self):
        """Start assertion then clause (REST Assured pattern)"""
        return self
    
    def with_headers(self, headers: Dict[str, str]) -> 'RestApiClient':
        """Add custom headers to request"""
        self.session.headers.update(headers)
        logger.debug(f"Headers updated: {headers}")
        return self
    
    def with_auth(self, token: str) -> 'RestApiClient':
        """Add Bearer token authentication"""
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
        logger.debug("Bearer token authentication added")
        return self
    
    def with_basic_auth(self, username: str, password: str) -> 'RestApiClient':
        """Add basic authentication"""
        self.session.auth = (username, password)
        logger.debug(f"Basic auth added for user: {username}")
        return self
    
    def with_query_params(self, params: Dict[str, Any]) -> 'RestApiClient':
        """Store query parameters for request"""
        self._query_params = params
        logger.debug(f"Query params set: {params}")
        return self
    
    def with_body(self, body: Dict[str, Any]) -> 'RestApiClient':
        """Store request body"""
        self._body = body
        logger.debug(f"Request body set: {body}")
        return self
    
    def with_json(self, json_data: Dict[str, Any]) -> 'RestApiClient':
        """Store JSON payload (alias for with_body)"""
        return self.with_body(json_data)
    
    def with_form_data(self, form_data: Dict[str, Any]) -> 'RestApiClient':
        """Store form data"""
        self._form_data = form_data
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded"
        })
        logger.debug(f"Form data set: {form_data}")
        return self
    
    def with_timeout(self, timeout: int) -> 'RestApiClient':
        """Set custom timeout for request"""
        self.timeout = timeout
        logger.debug(f"Timeout set to: {timeout}s")
        return self
    
    # ==================== HTTP METHODS ====================
    
    def get(self, endpoint: str, **kwargs) -> 'RestApiClient':
        """Execute GET request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        
        params = getattr(self, '_query_params', None)
        self.response = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
        
        self._log_request("GET", endpoint)
        return self
    
    def post(self, endpoint: str, **kwargs) -> 'RestApiClient':
        """Execute POST request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        
        body = getattr(self, '_body', None)
        form_data = getattr(self, '_form_data', None)
        
        if form_data:
            self.response = self.session.post(url, data=form_data, timeout=self.timeout, **kwargs)
        else:
            self.response = self.session.post(url, json=body, timeout=self.timeout, **kwargs)
        
        self._log_request("POST", endpoint, body)
        return self
    
    def put(self, endpoint: str, **kwargs) -> 'RestApiClient':
        """Execute PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        
        body = getattr(self, '_body', None)
        self.response = self.session.put(url, json=body, timeout=self.timeout, **kwargs)
        
        self._log_request("PUT", endpoint, body)
        return self
    
    def patch(self, endpoint: str, **kwargs) -> 'RestApiClient':
        """Execute PATCH request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH {url}")
        
        body = getattr(self, '_body', None)
        self.response = self.session.patch(url, json=body, timeout=self.timeout, **kwargs)
        
        self._log_request("PATCH", endpoint, body)
        return self
    
    def delete(self, endpoint: str, **kwargs) -> 'RestApiClient':
        """Execute DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        
        self.response = self.session.delete(url, timeout=self.timeout, **kwargs)
        
        self._log_request("DELETE", endpoint)
        return self
    
    # ==================== ASSERTIONS ====================
    
    def status_code(self, expected_code: int) -> 'RestApiClient':
        """Assert response status code"""
        actual_code = self.response.status_code
        assert actual_code == expected_code, \
            f"Expected status {expected_code}, got {actual_code}. Response: {self.response.text}"
        logger.info(f"✓ Status code assertion passed: {expected_code}")
        return self
    
    def status_is_ok(self) -> 'RestApiClient':
        """Assert response status is 200 OK"""
        return self.status_code(200)
    
    def status_is_created(self) -> 'RestApiClient':
        """Assert response status is 201 Created"""
        return self.status_code(201)
    
    def status_is_bad_request(self) -> 'RestApiClient':
        """Assert response status is 400 Bad Request"""
        return self.status_code(400)
    
    def status_is_unauthorized(self) -> 'RestApiClient':
        """Assert response status is 401 Unauthorized"""
        return self.status_code(401)
    
    def status_is_forbidden(self) -> 'RestApiClient':
        """Assert response status is 403 Forbidden"""
        return self.status_code(403)
    
    def status_is_not_found(self) -> 'RestApiClient':
        """Assert response status is 404 Not Found"""
        return self.status_code(404)
    
    def has_header(self, header_name: str, header_value: Optional[str] = None) -> 'RestApiClient':
        """Assert response has specific header"""
        assert header_name in self.response.headers, \
            f"Header '{header_name}' not found in response"
        
        if header_value:
            actual_value = self.response.headers.get(header_name)
            assert actual_value == header_value, \
                f"Header '{header_name}' has value '{actual_value}', expected '{header_value}'"
        
        logger.info(f"✓ Header assertion passed: {header_name}")
        return self
    
    def content_type(self, expected_type: str) -> 'RestApiClient':
        """Assert response content type"""
        return self.has_header("Content-Type", expected_type)
    
    def body_contains_key(self, key: str) -> 'RestApiClient':
        """Assert response body contains key"""
        data = self.get_json_response()
        assert key in data, f"Key '{key}' not found in response body: {data}"
        logger.info(f"✓ Body contains key assertion passed: {key}")
        return self
    
    def body_contains_keys(self, *keys) -> 'RestApiClient':
        """Assert response body contains all keys"""
        data = self.get_json_response()
        for key in keys:
            assert key in data, f"Key '{key}' not found in response body: {data}"
        logger.info(f"✓ Body contains keys assertion passed: {keys}")
        return self
    
    def body_equals(self, expected_body: Dict[str, Any]) -> 'RestApiClient':
        """Assert response body equals expected"""
        actual_body = self.get_json_response()
        assert actual_body == expected_body, \
            f"Body mismatch. Expected: {expected_body}, Got: {actual_body}"
        logger.info("✓ Body equals assertion passed")
        return self
    
    def body_path_has_value(self, json_path: str, expected_value: Any) -> 'RestApiClient':
        """Assert specific JSON path has value"""
        data = self.get_json_response()
        
        # Simple JSON path navigation (dot notation)
        keys = json_path.split(".")
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                value = None
                break
        
        assert value == expected_value, \
            f"Path '{json_path}' has value '{value}', expected '{expected_value}'"
        logger.info(f"✓ Body path assertion passed: {json_path} = {expected_value}")
        return self
    
    def response_time_less_than(self, milliseconds: int) -> 'RestApiClient':
        """Assert response time is less than milliseconds"""
        actual_time = self.response.elapsed.total_seconds() * 1000
        assert actual_time < milliseconds, \
            f"Response time {actual_time}ms exceeds limit {milliseconds}ms"
        logger.info(f"✓ Response time assertion passed: {actual_time}ms < {milliseconds}ms")
        return self
    
    # ==================== RESPONSE EXTRACTION ====================
    
    def get_status_code(self) -> int:
        """Get response status code"""
        return self.response.status_code
    
    def get_json_response(self) -> Dict[str, Any]:
        """Get response as JSON"""
        try:
            return self.response.json()
        except json.JSONDecodeError:
            raise AssertionError(f"Response is not valid JSON: {self.response.text}")
    
    def get_text_response(self) -> str:
        """Get response as text"""
        return self.response.text
    
    def get_response_body(self) -> Dict[str, Any]:
        """Alias for get_json_response"""
        return self.get_json_response()
    
    def get_header(self, header_name: str) -> Optional[str]:
        """Get specific response header"""
        return self.response.headers.get(header_name)
    
    def get_response_time(self) -> float:
        """Get response time in seconds"""
        return self.response.elapsed.total_seconds()
    
    # ==================== UTILITY METHODS ====================
    
    def _log_request(self, method: str, endpoint: str, body: Optional[Dict] = None):
        """Log request details"""
        status = self.response.status_code
        logger.info(f"{method} {endpoint} - Status: {status}")
        if body:
            logger.debug(f"Request body: {body}")
        logger.debug(f"Response: {self.response.text[:500]}")  # First 500 chars
    
    def clear_headers(self) -> 'RestApiClient':
        """Clear custom headers"""
        self.session.headers.clear()
        self.session.headers.update(DEFAULT_HEADERS)
        logger.debug("Headers cleared")
        return self
    
    def reset(self) -> 'RestApiClient':
        """Reset client state"""
        self._query_params = {}
        self._body = {}
        self._form_data = {}
        self.response = None
        return self
    
    def close(self):
        """Close session"""
        self.session.close()
        logger.info("Session closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class BaseAPITest:
    """Base class for API tests - provides helper methods"""
    
    def setup_method(self):
        """Setup before each test"""
        self.client = RestApiClient()
    
    def teardown_method(self):
        """Teardown after each test"""
        self.client.close()
    
    @staticmethod
    def create_client() -> RestApiClient:
        """Create a new REST API client"""
        return RestApiClient()
