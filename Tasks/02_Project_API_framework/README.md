# REST API Testing Framework

A comprehensive, production-ready REST API testing framework using Python `requests` library with REST Assured style fluent API.

## Overview

This framework implements REST Assured principles using Python, providing:
- ✅ **Fluent API** - Given-When-Then style (REST Assured pattern)
- ✅ **Comprehensive Assertions** - Status, headers, body, response time
- ✅ **Request Building** - Headers, auth, query params, body, timeouts
- ✅ **Response Handling** - JSON, text, headers extraction
- ✅ **Pytest Integration** - Fixtures, markers, parameterization
- ✅ **Logging & Debugging** - Detailed request/response logging
- ✅ **Configuration Management** - Externalized settings and credentials
- ✅ **CI/CD Ready** - Reports, coverage, parallel execution

## Architecture

```
REST API Framework
├── config.py                # Configuration and constants
├── rest_client.py           # REST API client with fluent API
├── conftest.py              # Pytest fixtures and setup
├── test_auth_endpoints.py   # Test implementations
├── requirements.txt         # Dependencies
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your configuration
# Edit .env and set BASE_URL, TEST_EMAIL, TEST_PASSWORD
```

## Configuration

### Setup `.env` file

```bash
# API Configuration
BASE_URL=https://stage-api.careercounsel.ai
ENVIRONMENT=staging

# Test Credentials
TEST_EMAIL=pooja.tiwari+test@techverito.com
TEST_OTP=123456
TEST_PASSWORD=your_password

# Request Configuration
REQUEST_TIMEOUT=10

# Logging
LOG_LEVEL=INFO
```

### Update `config.py`

Configure API endpoints and constants:

```python
ENDPOINTS = {
    "login": "/user/login",
    "login_with_otp": "/user/login-with-otp",
    "logout": "/user/logout",
    "is_admin": "/user/me/is-admin",
    "is_test_user": "/user/me/is-test-user",
}
```

## Usage

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_auth_endpoints.py

# Run specific test class
pytest test_auth_endpoints.py::TestUserLogin

# Run specific test
pytest test_auth_endpoints.py::TestUserLogin::test_login_success

# Run with specific marker
pytest -m smoke      # Run only smoke tests
pytest -m functional # Run functional tests
pytest -m auth       # Run auth tests

# Run with coverage
pytest --cov=. --cov-report=html

# Run in parallel
pytest -n auto

# Run with HTML report
pytest --html=report.html
```

## Framework Usage Examples

### Basic GET Request

```python
def test_get_user(api_client):
    """Example: Basic GET request"""
    api_client.given() \
        .when() \
        .get("/user/123") \
        .then() \
        .status_code(200) \
        .body_contains_key("id")
```

### POST with Authentication

```python
def test_login(api_client):
    """Example: POST with authentication"""
    api_client.given() \
        .with_json({"email": "user@test.com", "password": "pass"}) \
        .when() \
        .post("/user/login") \
        .then() \
        .status_is_ok() \
        .body_contains_key("token")
```

### With Bearer Token

```python
def test_protected_endpoint(api_client, auth_token):
    """Example: Protected endpoint with bearer token"""
    api_client.given() \
        .with_auth(auth_token) \
        .when() \
        .get("/user/me") \
        .then() \
        .status_is_ok() \
        .content_type("application/json")
```

### With Query Parameters

```python
def test_search(api_client):
    """Example: Request with query parameters"""
    api_client.given() \
        .with_query_params({"q": "search", "page": 1}) \
        .when() \
        .get("/search") \
        .then() \
        .status_is_ok()
```

### Parameterized Testing

```python
@pytest.mark.parametrize("email,password,expected_status", [
    ("valid@test.com", "correct", 200),
    ("valid@test.com", "wrong", 401),
    ("", "correct", 400),
])
def test_login_variants(api_client, email, password, expected_status):
    """Example: Data-driven testing"""
    api_client.given() \
        .with_json({"email": email, "password": password}) \
        .when() \
        .post("/user/login") \
        .then() \
        .status_code(expected_status)
```

### Response Extraction

```python
def test_extract_response(api_client):
    """Example: Extract response data"""
    api_client.given() \
        .when() \
        .get("/user/123") \
        .then() \
        .status_is_ok()
    
    # Extract response data
    response_body = api_client.get_response_body()
    user_id = response_body.get("id")
    status_code = api_client.get_status_code()
    response_time = api_client.get_response_time()
```

## REST Client API

### Request Building Methods

```python
# Set custom headers
.with_headers({"X-Custom": "value"})

# Add bearer token authentication
.with_auth("token_string")

# Add basic authentication
.with_basic_auth("username", "password")

# Set query parameters
.with_query_params({"key": "value"})

# Set JSON body
.with_json({"key": "value"})
.with_body({"key": "value"})  # Alias

# Set form data
.with_form_data({"field": "value"})

# Set custom timeout
.with_timeout(30)
```

### HTTP Methods

```python
# GET request
.get("/endpoint")

# POST request
.post("/endpoint")

# PUT request
.put("/endpoint")

# PATCH request
.patch("/endpoint")

# DELETE request
.delete("/endpoint")
```

### Assertion Methods

```python
# Status code assertions
.status_code(200)
.status_is_ok()           # 200
.status_is_created()      # 201
.status_is_bad_request()  # 400
.status_is_unauthorized() # 401
.status_is_forbidden()    # 403
.status_is_not_found()    # 404

# Header assertions
.has_header("Content-Type")
.has_header("X-Custom", "value")
.content_type("application/json")

# Body assertions
.body_contains_key("id")
.body_contains_keys("id", "name", "email")
.body_equals({"key": "value"})
.body_path_has_value("user.email", "user@test.com")

# Response time assertions
.response_time_less_than(5000)  # milliseconds
```

### Response Extraction Methods

```python
# Get status code
status = api_client.get_status_code()

# Get response as JSON
data = api_client.get_json_response()
data = api_client.get_response_body()

# Get response as text
text = api_client.get_text_response()

# Get specific header
content_type = api_client.get_header("Content-Type")

# Get response time (seconds)
time_sec = api_client.get_response_time()
```

## Fixtures

### Available Fixtures

```python
# API client for making requests
def test_example(api_client):
    pass

# Test credentials
def test_example(test_credentials):
    email = test_credentials["email"]
    password = test_credentials["password"]

# Valid authentication token
def test_example(auth_token):
    pass

# Invalid token for negative testing
def test_example(invalid_token):
    pass

# Pre-authenticated client
def test_example(logged_in_client):
    pass
```

## Project Structure

```
02_Project_API_framework/
├── config.py                     # Configuration and constants
├── rest_client.py               # REST API client implementation
├── conftest.py                  # Pytest fixtures
├── test_auth_endpoints.py       # Authentication tests
├── requirements.txt             # Dependencies
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment variables template
├── .gitignore                   # Git exclusion rules
└── README.md                    # Documentation
```

## Test Organization

Tests are organized by endpoint and type:

```python
class TestUserLogin:
    @pytest.mark.smoke
    def test_login_success(self):
        """Positive test"""
        
    @pytest.mark.functional
    def test_login_variants(self):
        """Data-driven test"""
        
    @pytest.mark.auth
    def test_login_missing_token(self):
        """Authentication test"""
        
    @pytest.mark.error
    def test_login_invalid_input(self):
        """Error handling test"""
        
    @pytest.mark.edge
    def test_login_boundary(self):
        """Edge case test"""
```

## Test Markers

Use markers to organize and run specific test types:

```bash
pytest -m smoke       # Smoke tests
pytest -m functional  # Functional tests
pytest -m auth        # Authentication tests
pytest -m error       # Error handling tests
pytest -m edge        # Edge case tests
```

## Logging

Logging is configured to show request/response details:

```
INFO:rest_client:GET /user/login - Status: 200
DEBUG:rest_client:Request body: {"email": "test@example.com"}
DEBUG:rest_client:Response: {"token": "abc123", ...}
```

Configure log level in `.env`:

```bash
LOG_LEVEL=DEBUG  # Shows detailed request/response
LOG_LEVEL=INFO   # Shows summary only
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: API Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest --junitxml=results.xml --cov=. --cov-report=xml
```

### Jenkins Example

```groovy
stage('Test') {
    steps {
        sh 'pip install -r requirements.txt'
        sh 'pytest --html=report.html --cov=.'
    }
}
```

## Best Practices

1. ✅ **Fluent API** - Use given().when().then() pattern
2. ✅ **Reusable Fixtures** - Use pytest fixtures for setup
3. ✅ **Clear Naming** - Descriptive test names with scenario
4. ✅ **Parameterization** - Use @pytest.mark.parametrize
5. ✅ **No Hardcoding** - Use config.py and fixtures
6. ✅ **Assertions** - Clear and specific assertions
7. ✅ **Logging** - Enable debug logging for troubleshooting
8. ✅ **Documentation** - Docstrings on every test

## Troubleshooting

### Connection Errors

```bash
# Check if API is running
curl https://stage-api.careercounsel.ai/docs

# Verify BASE_URL in .env
cat .env | grep BASE_URL
```

### Import Errors

```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Verify you're in virtual environment
source venv/bin/activate
```

### Test Failures

1. Check test credentials in `.env`
2. Verify API endpoint is correct
3. Check authentication token is valid
4. Enable DEBUG logging: `LOG_LEVEL=DEBUG`

## Contributing

When adding new tests:
1. Follow the same structure and naming
2. Include docstrings
3. Use markers for test categorization
4. Add both positive and negative scenarios
5. Test edge cases

## References

- **REST Assured (Java)**: https://rest-assured.io/
- **Requests Library**: https://requests.readthedocs.io/
- **Pytest Documentation**: https://docs.pytest.org/
- **API Documentation**: https://stage-api.careercounsel.ai/docs#/

## License

[Add your license here]

## Support

For issues or questions, refer to:
1. Check existing test examples
2. Enable debug logging
3. Review API documentation
4. Check error messages in test output
