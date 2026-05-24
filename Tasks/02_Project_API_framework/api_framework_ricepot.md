# REST API Framework Rice Pot Framework

## Purpose
Convert REST API framework requirements into a structured Rice Pot prompt that generates clear, reusable, and maintainable API testing frameworks using Python httpx.

---

## Rice Pot API Framework Template

### Role
**You are a QA engineer with 10+ years of experience in API testing, automation, and framework architecture.**

Your expertise includes:
- Designing scalable API testing frameworks
- Writing clean, maintainable Python code
- Understanding REST API specifications and httpx library
- Implementing reusable fixtures, configuration management, and helper methods
- Following SOLID principles and design patterns
- Building frameworks that are easy to extend and maintain

---

### Instruction
**Design and implement a REST API testing framework using Python httpx that supports functional testing, authentication, authorization, data validation, and comprehensive error handling.**

---

### Context
**Framework Requirements:**
- **HTTP Client Library:** Python httpx (synchronous and/or asynchronous)
- **Testing Framework:** Pytest with fixtures, parameterization, and markers
- **Project Structure:** Modular design with separation of concerns
- **API Documentation:** OpenAPI/Swagger specification (if available)
- **Test Credentials:** Centralized configuration management
- **Base URL:** Configurable environment-based URLs

**Key Constraints:**
- Write simple, understandable code (no overengineering)
- Follow DRY (Don't Repeat Yourself) principle
- Isolate tests - each test must run independently
- Use fixtures for shared resources (client, credentials, tokens)
- Implement reusable helper methods in base classes
- Manage configuration externally (not hardcoded)
- Support parameterized testing for data-driven scenarios
- Include comprehensive documentation and examples

**Architectural Principles:**
- Base Test Class: Common assertion methods and HTTP helpers
- Configuration Isolation: config.py for constants and credentials
- Fixture Management: conftest.py for shared pytest fixtures
- Endpoint Organization: One test class per endpoint
- Test Categories: Organize by functional, auth, error handling, edge cases

---

### Example
**Example Framework Structure:**

```
api_tests/
├── config.py                    # Configuration, constants, endpoints
├── conftest.py                  # Pytest fixtures and setup
├── base_test.py                 # Base class with helper methods
├── tests/
│   ├── test_auth.py             # Authentication tests
│   ├── test_users.py            # User endpoint tests
│   └── test_data.py             # Data validation tests
├── requirements.txt             # Dependencies
├── pytest.ini                   # Pytest configuration
└── README.md                    # Documentation
```

**Example Base Test Class:**

```python
# base_test.py
class BaseAPITest:
    """Base class with common helper methods"""
    
    @staticmethod
    def make_request(method, endpoint, **kwargs):
        """Make HTTP request and return response"""
        with httpx.Client(base_url=BASE_URL) as client:
            return getattr(client, method.lower())(endpoint, **kwargs)
    
    @staticmethod
    def assert_response_status(response, expected_status):
        """Assert response status code"""
        assert response.status_code == expected_status, \
            f"Expected {expected_status}, got {response.status_code}"
    
    @staticmethod
    def assert_response_has_key(response, key):
        """Assert response JSON has specific key"""
        data = response.json()
        assert key in data, f"Key '{key}' not found in response"
```

**Example Test Implementation:**

```python
# tests/test_users.py
class TestUserLogin(BaseAPITest):
    """Test suite for /user/login endpoint"""
    
    endpoint = "/user/login"
    
    def test_login_success(self, sync_client, test_credentials):
        """Positive test: Verify successful login returns token"""
        response = sync_client.post(
            self.endpoint,
            json=test_credentials
        )
        self.assert_response_status(response, 200)
        self.assert_response_has_key(response, "token")
    
    @pytest.mark.parametrize("email,password,expected", [
        ("valid@test.com", "correct", 200),
        ("valid@test.com", "wrong", 401),
        ("", "correct", 400),
    ])
    def test_login_variants(self, sync_client, email, password, expected):
        """Data-driven test with multiple inputs"""
        response = sync_client.post(
            self.endpoint,
            json={"email": email, "password": password}
        )
        self.assert_response_status(response, expected)
```

---

### Parameters

#### 1. Framework Architecture
- **Configuration Management**
  - Centralized config.py with BASE_URL, endpoints, credentials
  - Support for environment variables (.env file)
  - Constants for HTTP status codes
  - API timeout settings

- **Base Test Class**
  - Reusable HTTP request methods (GET, POST, PUT, DELETE, PATCH)
  - Common assertion methods (status, keys, schema, JSON structure)
  - Response parsing helpers
  - Error handling utilities

- **Fixtures (conftest.py)**
  - httpx.Client fixture for HTTP operations
  - Authentication token fixture
  - Test credentials fixture
  - Mock data fixtures
  - Setup/teardown for test isolation

#### 2. HTTP Client Integration (httpx)
- **Synchronous Client:** For blocking test operations
- **Request Building:** Headers, authentication, JSON payload
- **Error Handling:** Connection errors, timeouts, invalid responses
- **Response Handling:** JSON parsing, status codes, headers
- **Authentication:** Bearer token support, custom headers

#### 3. Test Organization
- **One Test Class Per Endpoint:** Clear separation of concerns
- **Test Categories:** Organized by functional, auth, error handling, edge cases
- **Test Naming:** `test_<endpoint>_<scenario>` convention
- **Parameterized Tests:** Multiple inputs using @pytest.mark.parametrize
- **Docstrings:** Clear description of test purpose

#### 4. Test Coverage Areas
- **Functional Testing:** Positive, negative, data validation
- **Authentication:** Token validation, missing headers, expired tokens
- **Authorization:** Role-based access, permission checks
- **Error Handling:** Invalid inputs, malformed data, boundary cases
- **HTTP Methods:** GET, POST, PUT, DELETE, PATCH validation
- **Response Validation:** Schema, data types, required fields

#### 5. Best Practices
- No hardcoded credentials
- Each test isolated and independent
- Fixture-based setup/teardown
- Clear error messages in assertions
- Comprehensive documentation
- Support for parallel test execution
- CI/CD integration ready

---

### Output
**Deliverable:** A complete REST API testing framework with:

**Core Files:**
1. **config.py** - API URLs, endpoints, credentials, constants
2. **conftest.py** - Pytest fixtures and configuration
3. **base_test.py** - Base test class with helper methods
4. **test_*.py** - Individual endpoint test modules

**Documentation:**
- **README.md** - Complete setup and usage guide
- **QUICKSTART.md** - 5-minute quick start guide
- **pytest.ini** - Pytest configuration

**Configuration Files:**
- **requirements.txt** - All dependencies
- **.env.example** - Environment variables template
- **.gitignore** - Files to exclude from version control

**Features Included:**
- ✅ Modular, extensible architecture
- ✅ Reusable fixtures and helper methods
- ✅ Parameterized testing support
- ✅ Configuration management
- ✅ Comprehensive error handling
- ✅ Ready for CI/CD integration
- ✅ Full documentation with examples
- ✅ Support for async/sync httpx clients

---

### Tone
- **Professional:** Use standard QA and engineering terminology
- **Practical:** Focus on implementable solutions with working examples
- **Educational:** Explain design decisions and best practices
- **Direct:** Clear, concise instructions without unnecessary fluff
- **Scalable:** Show how to extend framework for new endpoints

---

## Reusable Prompt for API Framework Development

Use this template when creating REST API testing frameworks:

```
Role: You are a QA engineer with 10+ years of experience in API testing, automation, and framework architecture.

Instruction: Design and implement a REST API testing framework using Python httpx that supports functional testing, authentication, authorization, data validation, and comprehensive error handling.

Context:
- HTTP Client: Python httpx (version 0.23.0+)
- Testing Framework: Pytest with fixtures, parameterization, and markers
- API Type: RESTful API with JSON request/response
- Base URL: [SPECIFY BASE URL]
- Authentication: [SPECIFY AUTH TYPE - Bearer token, API key, etc.]
- Available Endpoints: [LIST ENDPOINTS]
- Test Credentials: [PROVIDE TEST CREDENTIALS]
- Project Structure: Modular with separation of concerns

Example:
[PROVIDE EXAMPLE TEST CASE]
[PROVIDE EXAMPLE FRAMEWORK STRUCTURE]

Parameters:
1. Framework Architecture: Base class, fixtures, configuration management, modular design
2. HTTP Operations: Request building, response handling, error management, timeouts
3. Test Organization: One class per endpoint, clear naming, categories (functional, auth, error)
4. Test Coverage: Positive, negative, data validation, authentication, authorization, edge cases
5. Documentation: README, QUICKSTART, inline comments, docstrings
6. Best Practices: DRY principle, fixture-based setup, parameterized tests, no hardcoded data

Output: Complete REST API testing framework including:
- Core framework files (config, conftest, base_test)
- Test implementations for all endpoints
- Configuration and setup files
- Comprehensive documentation
- CI/CD ready structure

Tone: Professional, practical, educational, and direct.
```

---

## API Framework Architecture Patterns

### Pattern 1: Simple Synchronous Framework
```python
# Minimal setup for synchronous testing
class BaseAPITest:
    def make_request(self, method, endpoint, **kwargs):
        with httpx.Client(base_url=BASE_URL) as client:
            return getattr(client, method.lower())(endpoint, **kwargs)

class TestEndpoint(BaseAPITest):
    def test_operation(self, sync_client):
        response = sync_client.post("/endpoint", json=payload)
        assert response.status_code == 200
```

### Pattern 2: Advanced with Fixtures
```python
# conftest.py - Reusable fixtures
@pytest.fixture
def sync_client():
    with httpx.Client(base_url=BASE_URL, headers=DEFAULT_HEADERS) as client:
        yield client

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

# Test usage
class TestEndpoint(BaseAPITest):
    def test_operation(self, sync_client, auth_headers):
        response = sync_client.post(
            "/endpoint",
            json=payload,
            headers=auth_headers
        )
        assert response.status_code == 200
```

### Pattern 3: Data-Driven Testing
```python
@pytest.mark.parametrize("input_data,expected_status", [
    ({"valid": "data"}, 200),
    ({"invalid": "data"}, 400),
    ({}, 400),
])
def test_operation(self, sync_client, input_data, expected_status):
    response = sync_client.post("/endpoint", json=input_data)
    assert response.status_code == expected_status
```

### Pattern 4: Error Handling & Assertions
```python
def test_with_assertions(self, sync_client):
    response = sync_client.get("/endpoint/123")
    
    # Status assertion
    self.assert_response_status(response, 200)
    
    # Key assertions
    self.assert_response_has_key(response, "id")
    self.assert_response_keys(response, ["id", "name", "email"])
    
    # Custom assertions
    data = self.get_response_json(response)
    assert isinstance(data["id"], int)
    assert len(data["name"]) > 0
```

---

## Framework Checklist

Before finalizing your API framework, verify:

- [ ] **Configuration:** Base URL, endpoints, credentials externalized
- [ ] **Base Class:** Common assertion and helper methods implemented
- [ ] **Fixtures:** Setup/teardown, client, credentials, auth tokens
- [ ] **Test Organization:** One class per endpoint, clear naming
- [ ] **Test Coverage:** Functional, auth, error handling, edge cases
- [ ] **Parameterization:** Data-driven tests for multiple inputs
- [ ] **Documentation:** README, QUICKSTART, docstrings
- [ ] **Error Handling:** Graceful failure messages, detailed assertions
- [ ] **Independence:** Tests run in any order without dependencies
- [ ] **CI/CD Ready:** No hardcoded paths, configurable environments

---

## Implementation Steps

1. **Create Project Structure**
   - Set up folder layout (config, tests, fixtures)
   - Create virtual environment and install dependencies

2. **Implement Configuration**
   - Define BASE_URL, endpoints, credentials
   - Create config.py with constants

3. **Build Base Test Class**
   - Implement helper methods
   - Add common assertions
   - Create HTTP request wrapper

4. **Create Fixtures**
   - httpx Client fixture
   - Authentication token fixture
   - Test data fixtures

5. **Implement Tests**
   - One test class per endpoint
   - Organize by test type (functional, auth, error)
   - Use parameterization for data-driven tests

6. **Add Documentation**
   - README with setup and usage
   - QUICKSTART guide
   - Docstrings in code

7. **Configure CI/CD**
   - Add pytest.ini configuration
   - Setup GitHub Actions or Jenkins
   - Configure coverage reporting

---

## Common Pitfalls to Avoid

❌ **Hardcoded Credentials** → Use config.py and fixtures  
❌ **Test Dependencies** → Each test must be independent  
❌ **Duplicate Code** → Use base class and fixtures  
❌ **Unclear Test Names** → Use descriptive names with scenarios  
❌ **No Error Context** → Provide detailed assertion messages  
❌ **Missing Documentation** → Document code and framework usage  
❌ **Tight Coupling** → Use configuration and dependency injection  

---

## References

- **httpx Documentation**: https://www.python-httpx.org/
- **Pytest Documentation**: https://docs.pytest.org/
- **REST API Best Practices**: https://restfulapi.net/
- **Python Testing Patterns**: https://docs.pytest.org/en/latest/example/index.html

