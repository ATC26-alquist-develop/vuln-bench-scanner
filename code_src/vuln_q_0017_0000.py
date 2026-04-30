```python
import os
import hashlib
import hmac
import secrets
import time
from typing import Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class SecureLoginSystem:
    def __init__(self):
        # Use environment variables for sensitive data
        self._secret_key = os.environ.get('SECRET_KEY')
        if not self._secret_key:
            raise ValueError("SECRET_KEY environment variable must be set")
        
        # Generate secure random salt
        self._salt = os.urandom(32)
        
        # Generate secure encryption key
        self._key = self._generate_key()
        
        # Secure cookie settings
        self._cookie_secure = True
        self._cookie_http_only = True
        self._cookie_max_age = 3600  # 1 hour
        
        # Secure storage for user data
        self._users: Dict[str, Dict[str, str]] = {}
        
        # Secure session storage
        self._sessions: Dict[str, Dict[str, str]] = {}
        
        # Secure key derivation function
        self._kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=100000,
            backend=default_backend()
        )
        
        # Secure encryption
        self._fernet = Fernet(self._key)
        
    def _generate_key(self) -> bytes:
        """Generate a secure encryption key using PBKDF2."""
        return base64.urlsafe_b64encode(self._kdf.derive(self._secret_key.encode()))
    
    def _hash_password(self, password: str) -> str:
        """Securely hash password using Argon2."""
        return hashlib.argon2.using(rounds=10, memory_cost=65536, parallelism=4).hash(password)
    
    def register(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        if not username or not password:
            return False
            
        if username in self._users:
            return False
            
        hashed_password = self._hash_password(password)
        self._users[username] = {'password': hashed_password}
        return True
    
    def login(self, username: str, password: str) -> Optional[str]:
        """Securely authenticate user and create session."""
        if not username or not password:
            return None
            
        if username not in self._users:
            return None
            
        stored_password = self._users[username]['password']
        if not self._verify_password(password, stored_password):
            return None
            
        session_id = secrets.token_urlsafe(32)
        self._sessions[session_id] = username
        return session_id
    
    def logout(self, session_id: str) -> None:
        """Securely invalidate a user session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
    
    def is_authenticated(self, session_id: str) -> bool:
        """Check if a session is valid."""
        return session_id in self._sessions
    
    def get_user(self, session_id: str) -> Optional[str]:
        """Get username from session."""
        if self.is_authenticated(session_id):
            return self._sessions[session_id]
        return None
    
    def set_secure_cookie(self, session_id: str) -> str:
        """Set secure cookie with session ID."""
        if not session_id:
            return ''
            
        cookie_value = session_id
        cookie = self._fernet.encrypt(cookie_value.encode())
        return f"{cookie.decode()}; HttpOnly