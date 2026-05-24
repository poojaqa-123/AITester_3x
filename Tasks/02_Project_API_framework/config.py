"""
REST API Framework Configuration
Base URL, endpoints, credentials, and constants
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================== API CONFIGURATION ====================

BASE_URL = os.getenv("BASE_URL", "https://stage-api.careercounsel.ai")
API_DOCS_URL = "https://stage-api.careercounsel.ai/docs#/"
ENVIRONMENT = os.getenv("ENVIRONMENT", "staging")

# ==================== TEST CREDENTIALS ====================

TEST_EMAIL = os.getenv("TEST_EMAIL", "pooja.tiwari+test@techverito.com")
TEST_OTP = os.getenv("TEST_OTP", "123456")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "correct_password")

# ==================== HTTP CONFIGURATION ====================

DEFAULT_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "RestAPI-Test-Framework/1.0"
}

# ==================== ENDPOINTS ====================

ENDPOINTS = {
    # Authentication
    "login": "/user/login",
    "login_with_otp": "/user/login-with-otp",
    "logout": "/user/logout",
    
    # User Information
    "is_admin": "/user/me/is-admin",
    "is_test_user": "/user/me/is-test-user",
    "get_profile": "/user/me",
    
    # Add more endpoints as needed
}

# ==================== HTTP STATUS CODES ====================

# Success Responses
STATUS_OK = 200
STATUS_CREATED = 201
STATUS_ACCEPTED = 202
STATUS_NO_CONTENT = 204

# Client Error Responses
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404
STATUS_CONFLICT = 409
STATUS_UNPROCESSABLE_ENTITY = 422

# Server Error Responses
STATUS_INTERNAL_SERVER_ERROR = 500
STATUS_BAD_GATEWAY = 502
STATUS_SERVICE_UNAVAILABLE = 503

# ==================== REQUEST/RESPONSE CONSTANTS ====================

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_FORM = "application/x-www-form-urlencoded"
BEARER_SCHEME = "Bearer"

# ==================== RETRY CONFIGURATION ====================

MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]

# ==================== LOGGING ====================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==================== VALIDATION ====================

# Email regex pattern
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# OTP should be 6 digits
OTP_REGEX = r"^\d{6}$"

# Token should be non-empty string
MIN_TOKEN_LENGTH = 20
