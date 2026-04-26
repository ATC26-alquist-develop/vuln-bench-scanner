```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets
import re
from typing import Optional
from datetime import datetime, timedelta
import time
from dataclasses import dataclass
from enum import Enum
import logging
from functools import wraps

# Configure secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('secure_login')

class LoginStatus(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_DISABLED = "account_disabled"
    RATE_LIMITED = "rate_limited"

@dataclass
class LoginResult:
    status: LoginStatus
    message: str
    user_id: Optional[str] = None

class SecureLoginSystem:
    def __init__(self):
        self._ph = PasswordHasher()
        self._users = {}  # In production, use secure database
        self._login_attempts = {}
        self._max_attempts = 5
        self._lockout_duration = 300  # 5 minutes
        self._session_duration = 3600  # 1 hour
        
    def _validate_username(self, username: str) -> bool:
        """Validate username format"""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,32}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

    def register_user(self, username: str, password: str) -> LoginResult:
        """Register a new user with secure password hashing"""
        if not self._validate_username(username) or not self._validate_password(password):
            return LoginResult(
                status=LoginStatus.INVALID_CREDENTIALS,
                message="Invalid username or password format"
            )
            
        if username in self._users:
            return LoginResult(
                status=LoginStatus.INVALID_CREDENTIALS,
                message="Username already exists"
            )
            
        try:
            hashed_password = self._ph.hash(password)
            self._users[username] = hashed_password
            logger.info(f"User registered: {username}")
            return LoginResult(status=LoginStatus.SUCCESS, message="User registered successfully")
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return LoginResult(status=LoginStatus.INVALID_CREDENTIALS, message="Registration failed")

    def login(self, username: str, password: str) -> LoginResult:
        """Perform secure login"""
        if not self._validate_username(username) or not self._validate_password(password):
            return LoginResult(
                status=LoginStatus.INVALID_CREDENTIALS,
                message="Invalid username or password format"
            )

        current_time = time.time()
        
        # Check for account lockout
        if username in self._login_attempts:
            attempts, last_attempt = self._login_attempts[username]
            if attempts >= self._max_attempts and current_time - last_attempt < self._lockout_duration:
                return LoginResult(
                    status=LoginStatus.ACCOUNT_DISABLED,
                    message="Account temporarily disabled due to too many failed attempts"
                )
            
        # Check if user exists
        if username not in self._users:
            return LoginResult(
                status=LoginStatus.INVALID_CREDENTIALS,
                message="Invalid username or password"
            )
            
        try:
            self._ph.verify(self._users[username], password)
            logger.info(f"User logged in: {username}")
            
            # Generate secure session token
            session_token = secrets.token_urlsafe(32)
            expiration = current_time + self._session_duration
            
            # Store session (in