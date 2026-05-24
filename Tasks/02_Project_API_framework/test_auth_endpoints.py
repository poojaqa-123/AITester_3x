"""
Test suite for User Authentication endpoints
Reference: https://stage-api.careercounsel.ai/docs#/
"""
import pytest
from rest_client import BaseAPITest
from config import (
    ENDPOINTS, STATUS_OK, STATUS_UNAUTHORIZED, STATUS_BAD_REQUEST,
    TEST_EMAIL, TEST_PASSWORD
)


class TestUserLogin(BaseAPITest):
    """Test suite for /user/login endpoint"""
    
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_login_success(self, api_client, test_credentials):
        """Positive test: Verify successful login returns 200 OK with token"""
        api_client.given() \
            .with_json({"email": TEST_EMAIL, "password": TEST_PASSWORD}) \
            .when() \
            .post(ENDPOINTS["login"]) \
            .then() \
            .status_code(STATUS_OK) \
            .body_contains_key("token")
    
    @pytest.mark.functional
    @pytest.mark.parametrize("email,password,expected_status", [
        (TEST_EMAIL, TEST_PASSWORD, 200),
        (TEST_EMAIL, "wrong_password", 401),
        ("", TEST_PASSWORD, 400),
        (TEST_EMAIL, "", 400),
        ("invalid_email", TEST_PASSWORD, 400),
    ])
    def test_login_variants(self, api_client, email, password, expected_status):
        """Data-driven test with multiple input combinations"""
        api_client.given() \
            .with_json({"email": email, "password": password}) \
            .when() \
            .post(ENDPOINTS["login"]) \
            .then() \
            .status_code(expected_status)
    
    @pytest.mark.functional
    def test_login_wrong_password(self, api_client):
        """Negative test: Verify 401 Unauthorized with wrong password"""
        api_client.given() \
            .with_json({"email": TEST_EMAIL, "password": "wrong_password"}) \
            .when() \
            .post(ENDPOINTS["login"]) \
            .then() \
            .status_is_unauthorized()
    
    @pytest.mark.error
    def test_login_missing_email(self, api_client):
        """Error handling: Verify 400 when email is missing"""
        api_client.given() \
            .with_json({"password": TEST_PASSWORD}) \
            .when() \
            .post(ENDPOINTS["login"]) \
            .then() \
            .status_is_bad_request()
    
    @pytest.mark.error
    def test_login_missing_password(self, api_client):
        """Error handling: Verify 400 when password is missing"""
        api_client.given() \
            .with_json({"email": TEST_EMAIL}) \
            .when() \
            .post(ENDPOINTS["login"]) \
            .then() \
            .status_is_bad_request()
    
    @pytest.mark.error
    def test_login_empty_body(self, api_client):
        """Error handling: Verify 400 with empty body"""
        api_client.given() \
            .with_json({}) \
            .when() \
            .post(ENDPOINTS["login"]) \
            .then() \
            .status_is_bad_request()
    
    @pytest.mark.edge
    def test_login_response_schema(self, api_client):
        """Edge case: Verify response schema on success"""
        api_client.given() \
            .with_json({"email": TEST_EMAIL, "password": TEST_PASSWORD}) \
            .when() \
            .post(ENDPOINTS["login"]) \
            .then() \
            .status_is_ok() \
            .body_contains_keys("token", "user")
    
    @pytest.mark.edge
    def test_login_response_time(self, api_client):
        """Edge case: Verify response time is reasonable"""
        api_client.given() \
            .with_json({"email": TEST_EMAIL, "password": TEST_PASSWORD}) \
            .when() \
            .post(ENDPOINTS["login"]) \
            .then() \
            .response_time_less_than(5000)  # 5 seconds


class TestUserLoginWithOTP(BaseAPITest):
    """Test suite for /user/login-with-otp endpoint"""
    
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_login_with_otp_success(self, api_client):
        """Positive test: Verify successful OTP login"""
        api_client.given() \
            .with_json({"email": "pooja.tiwari+test@techverito.com", "otp": "123456"}) \
            .when() \
            .post(ENDPOINTS["login_with_otp"]) \
            .then() \
            .status_code(STATUS_OK) \
            .body_contains_key("token")
    
    @pytest.mark.functional
    @pytest.mark.parametrize("email,otp,expected_status", [
        ("pooja.tiwari+test@techverito.com", "123456", 200),
        ("pooja.tiwari+test@techverito.com", "000000", 401),
        ("", "123456", 400),
        ("pooja.tiwari+test@techverito.com", "", 400),
    ])
    def test_login_with_otp_variants(self, api_client, email, otp, expected_status):
        """Data-driven test with multiple OTP inputs"""
        api_client.given() \
            .with_json({"email": email, "otp": otp}) \
            .when() \
            .post(ENDPOINTS["login_with_otp"]) \
            .then() \
            .status_code(expected_status)
    
    @pytest.mark.error
    def test_login_with_otp_missing_fields(self, api_client):
        """Error handling: Missing required fields"""
        api_client.given() \
            .with_json({}) \
            .when() \
            .post(ENDPOINTS["login_with_otp"]) \
            .then() \
            .status_is_bad_request()


class TestUserLogout(BaseAPITest):
    """Test suite for /user/logout endpoint"""
    
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_logout_success(self, logged_in_client, auth_token):
        """Positive test: Verify successful logout"""
        logged_in_client.given() \
            .when() \
            .post(ENDPOINTS["logout"]) \
            .then() \
            .status_code(STATUS_OK)
    
    @pytest.mark.auth
    def test_logout_missing_token(self, api_client):
        """Auth test: Verify 401 when token is missing"""
        api_client.given() \
            .when() \
            .post(ENDPOINTS["logout"]) \
            .then() \
            .status_is_unauthorized()
    
    @pytest.mark.auth
    def test_logout_invalid_token(self, api_client, invalid_token):
        """Auth test: Verify 401 with invalid token"""
        api_client.given() \
            .with_auth(invalid_token) \
            .when() \
            .post(ENDPOINTS["logout"]) \
            .then() \
            .status_is_unauthorized()
    
    @pytest.mark.edge
    def test_logout_get_not_allowed(self, logged_in_client):
        """Edge case: Verify GET method not allowed"""
        logged_in_client.given() \
            .when() \
            .get(ENDPOINTS["logout"]) \
            .then() \
            .body_contains_key("error")  # Expect error response


class TestUserIsAdmin(BaseAPITest):
    """Test suite for /user/me/is-admin endpoint"""
    
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_is_admin_check(self, logged_in_client):
        """Positive test: Check admin status"""
        logged_in_client.given() \
            .when() \
            .get(ENDPOINTS["is_admin"]) \
            .then() \
            .status_code(STATUS_OK) \
            .body_contains_key("is_admin")
    
    @pytest.mark.auth
    def test_is_admin_missing_token(self, api_client):
        """Auth test: Verify 401 when token is missing"""
        api_client.given() \
            .when() \
            .get(ENDPOINTS["is_admin"]) \
            .then() \
            .status_is_unauthorized()
    
    @pytest.mark.auth
    def test_is_admin_invalid_token(self, api_client, invalid_token):
        """Auth test: Verify 401 with invalid token"""
        api_client.given() \
            .with_auth(invalid_token) \
            .when() \
            .get(ENDPOINTS["is_admin"]) \
            .then() \
            .status_is_unauthorized()


class TestUserIsTestUser(BaseAPITest):
    """Test suite for /user/me/is-test-user endpoint"""
    
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_is_test_user_check(self, logged_in_client):
        """Positive test: Check test user status"""
        logged_in_client.given() \
            .when() \
            .get(ENDPOINTS["is_test_user"]) \
            .then() \
            .status_code(STATUS_OK) \
            .body_contains_key("is_test_user")
    
    @pytest.mark.auth
    def test_is_test_user_missing_token(self, api_client):
        """Auth test: Verify 401 when token is missing"""
        api_client.given() \
            .when() \
            .get(ENDPOINTS["is_test_user"]) \
            .then() \
            .status_is_unauthorized()
    
    @pytest.mark.auth
    def test_is_test_user_invalid_token(self, api_client, invalid_token):
        """Auth test: Verify 401 with invalid token"""
        api_client.given() \
            .with_auth(invalid_token) \
            .when() \
            .get(ENDPOINTS["is_test_user"]) \
            .then() \
            .status_is_unauthorized()
