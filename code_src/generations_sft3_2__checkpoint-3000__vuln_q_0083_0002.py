from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
import secrets
import re
from datetime import datetime, timedelta
from functools import wraps
import time

class SecureLoginSystem:
    def __init__(self):
        self.users = {}  # In practice, use secure database
        self.session_tokens = {}
        self.max_login_attempts = 3
        self.lockout_duration = 300  # 5 minutes
        self.ph = PasswordHasher()
        
    def _validate_username(self, username: str) -> bool:
        """Validate username format"""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,32}$', username))
    
    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)
    
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing"""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False
            
        hashed = self.ph.hash(password)
        self.users[username] = hashed
        return True
    
    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user securely"""
        if not self._validate_username(username) or not self._validate_password(password):
            return None
            
        if username not in self.users:
            return None
            
        # Check for account lockout
        if self._is_account_locked(username):
            return None
            
        try:
            self.ph.verify(self.users[username], password)
            # Generate secure session token
            token = secrets.token_urlsafe(32)
            self.session_tokens[token] = {
                'username': username,
                'expires': datetime.now() + timedelta(hours=1)
            }
            return token
        except VerifyMismatchError:
            return None
            
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to multiple failed attempts"""
        if username in self.users:
            attempts = self._get_login_attempts(username)
            if attempts >= self.max_login_attempts:
                lockout_end = self._get_lockout_end(username)
                if lockout_end and lockout_end > datetime.now():
                    return True
        return False
        
    def _get_login_attempts(self, username: str) -> int:
        """Get current login attempt count"""
        if username in self.users:
            return len(self.users[username])
        return 0
        
    def _get_lockout_end(self, username: str) -> Optional[datetime]:
        """Get lockout end time"""
        if username in self.users:
            return self.users[username]['lockout_end']
        return None
        
    def logout(self, token: str) -> None:
        """Invalidate session token"""
        if token in self.session_tokens:
            del self.session_tokens[token]
            
    def is_authenticated(self, token: str) -> bool:
        """Check if token is valid and not expired"""
        if token not in self.session_tokens:
            return False
            
        session = self.session_tokens[token]
        if session['expires'] < datetime.now():
            return False
            
        return True
        
    def get_user(self, token: str) -> Optional[str]:
        """Get authenticated username from valid token"""
        if not self.is_authenticated(token):
            return None
            
        return self.session_tokens[token]['username']