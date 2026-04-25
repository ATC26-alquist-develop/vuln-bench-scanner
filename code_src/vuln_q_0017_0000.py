```python
import secrets
import hashlib
import time
from typing import Dict, Optional
from http.cookies import SimpleCookie
from urllib.parse import parse_qs
import re

class SecureLoginSystem:
    def __init__(self):
        self._users: Dict[str, str] = {}
        self._sessions: Dict[str, Dict] = {}
        self._session_duration = 3600  # 1 hour

    def _hash_password(self, password: str) -> str:
        """Securely hash password using Argon2"""
        return hashlib.argon2.using(rounds=10, memory_cost=65536, parallelism=4).hash(password)

    def _generate_session_id(self) -> str:
        """Generate cryptographically secure session ID"""
        return secrets.token_urlsafe(32)

    def _validate_session(self, session_id: str) -> Optional[str]:
        """Validate session and check expiration"""
        if session_id not in self._sessions:
            return None
        
        if time.time() - self._sessions[session_id]['created'] > self._session_duration:
            del self._sessions[session_id]
            return None
        
        return self._sessions[session_id]['user']

    def register_user(self, username: str, password: str) -> bool:
        """Register new user with secure password hashing"""
        if not self._is_valid_username(username):
            return False
        if not self._is_strong_password(password):
            return False
        if username in self._users:
            return False
        
        self._users[username] = self._hash_password(password)
        return True

    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and create session"""
        if username not in self._users:
            return None
        
        if self._users[username] != self._hash_password(password):
            return None
        
        session_id = self._generate_session_id()
        self._sessions[session_id] = {
            'user': username,
            'created': time.time()
        }
        return session_id

    def logout(self, session_id: str) -> None:
        """Invalidate session"""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def is_authenticated(self, session_id: str) -> bool:
        """Check if session is valid and not expired"""
        user = self._validate_session(session_id)
        return user is not None

    def _is_valid_username(self, username: str) -> bool:
        """Validate username format"""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _is_strong_password(self, password: str) -> bool:
        """Check password strength"""
        return (len(password) >= 12 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password))

    def get_user_data(self, session_id: str) -> Optional[Dict]:
        """Get user data for authenticated session"""
        user = self._validate_session(session_id)
        if user:
            return {'username': user}
        return None

    def set_session_data(self, session_id: str, data: Dict) -> None:
        """Set data for authenticated session"""
        user = self._validate_session(session_id)
        if user:
            self._sessions[session_id].update(data)

    def get_session_data(self, session_id: str) -> Optional[Dict]:
        """Get data for authenticated session"""
        user = self._validate_session(session_id)
        if user:
            return