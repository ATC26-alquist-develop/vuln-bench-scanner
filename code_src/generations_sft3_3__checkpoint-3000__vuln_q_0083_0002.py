```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
import secrets
import re
from datetime import datetime, timedelta
import time
from dataclasses import dataclass
from enum import Enum
import logging
from functools import wraps

# Configure secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthStatus(Enum):
    """Enum for authentication states"""
    SUCCESS = "success"
    FAILED_LOGIN_ATTEMPT = "failed_login_attempt"
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_DISABLED = "account_disabled"

@dataclass
class User:
    """Immutable user dataclass"""
    username: str
    password_hash: str
    created_at: datetime
    last_login: datetime = None

class SecureAuthSystem:
    def __init__(self):
        self.users = {}
        self.max_login_attempts = 5
        self.login_attempt_window = 300  # 5 minutes
        self.ph = PasswordHasher()
        
    def _validate_username(self, username: str) -> bool:
        """Validate username format"""
        if not isinstance(username, str):
            return False
        return bool(re.match(r'^[a-zA-Z0-9_]{3,32}$', username))
    
    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        if not isinstance(password, str) or len(password) < 12:
            return False
        return bool(re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()]).{12,}$', password))
    
    def register_user(self, username: str, password: str) -> AuthStatus:
        """Register a new user with secure password hashing"""
        try:
            if not self._validate_username(username) or not self._validate_password(password):
                return AuthStatus.INVALID_CREDENTIALS
                
            if username in self.users:
                return AuthStatus.INVALID_CREDENTIALS
                
            password_hash = self.ph.hash(password)
            self.users[username] = User(
                username=username,
                password_hash=password_hash,
                created_at=datetime.utcnow()
            )
            logger.info(f"User registered: {username}")
            return AuthStatus.SUCCESS
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return AuthStatus.INVALID_CREDENTIALS

    def authenticate(self, username: str, password: str) -> tuple[AuthStatus, Optional[str]]:
        """Authenticate user with secure password verification"""
        try:
            if not self._validate_username(username) or not self._validate_password(password):
                return AuthStatus.INVALID_CREDENTIALS, None
                
            user = self.users.get(username)
            if not user:
                return AuthStatus.INVALID_CREDENTIALS, None
                
            # Check if account is locked
            if self._is_account_locked(username):
                return AuthStatus.ACCOUNT_DISABLED, None
                
            try:
                self.ph.verify(user.password_hash, password)
                user.last_login = datetime.utcnow()
                logger.info(f"User authenticated: {username}")
                return AuthStatus.SUCCESS, username
                
            except VerifyMismatchError:
                # Increment failed attempts
                self._increment_failed_attempts(username)
                logger.warning(f"Failed login attempt for user: {username}")
                return AuthStatus.FAILED_LOGIN_ATTEMPT, None
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return AuthStatus.INVALID_CREDENTIALS, None

    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to too many failed attempts"""
        if username not in self.users:
            return False
            
        user = self.users[username]
        current_time = time.time