"""
Pytest configuration and shared fixtures for REST API tests
"""
import pytest
import logging
from rest_client import RestApiClient
from config import TEST_EMAIL, TEST_OTP, TEST_PASSWORD, BASE_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture(scope="session")
def test_credentials():
    """Fixture providing test credentials"""
    return {
        "email": TEST_EMAIL,
        "otp": TEST_OTP,
        "password": TEST_PASSWORD,
    }


@pytest.fixture
def api_client():
    """
    Fixture providing REST API client for each test.
    Automatically closes connection after test.
    """
    client = RestApiClient(base_url=BASE_URL)
    yield client
    client.close()


@pytest.fixture
def auth_token(api_client, test_credentials):
    """
    Fixture providing valid authentication token.
    This would typically login and return a token.
    """
    # Placeholder - in real scenario, call login endpoint
    return "valid_token_placeholder_12345"


@pytest.fixture
def invalid_token():
    """Fixture providing invalid token for negative testing"""
    return "invalid_token_xyz_12345"


@pytest.fixture
def logged_in_client(api_client, auth_token):
    """Fixture providing pre-authenticated API client"""
    api_client.with_auth(auth_token)
    return api_client


@pytest.fixture(autouse=True)
def reset_client(api_client):
    """Auto-reset client before each test"""
    api_client.reset()
    yield
    api_client.reset()


# ==================== PYTEST MARKERS ====================

def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests"
    )
    config.addinivalue_line(
        "markers", "functional: Functional tests"
    )
    config.addinivalue_line(
        "markers", "auth: Authentication tests"
    )
    config.addinivalue_line(
        "markers", "error: Error handling tests"
    )
    config.addinivalue_line(
        "markers", "edge: Edge case tests"
    )
