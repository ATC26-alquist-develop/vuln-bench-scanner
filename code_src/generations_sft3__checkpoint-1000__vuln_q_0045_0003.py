import secrets
import hashlib
import hmac
import time
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class User:
    username: str
    password_hash: str
    salt: str
    created_at: datetime
    last_login: datetime

class SecureAuthSystem:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.session_tokens: Dict[str, str] = {}
        self.session_expiry = timedelta(minutes=30)

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        if username in self.users:
            return False
        
        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password, salt)
        
        self.users[username] = User(
            username=username,
            password_hash=password_hash,
            salt=salt,
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        return True

    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate a user securely."""
        user = self.users.get(username)
        if not user:
            return None
        
        if self._verify_password(password, user.password_hash, user.salt):
            session_token = secrets.token_urlsafe(32)
            self.session_tokens[session_token] = username
            return session_token
        return None

    def validate_session(self, session_token: str) -> Optional[str]:
        """Validate a session token."""
        username = self.session_tokens.get(session_token)
        if not username:
            return None
            
        # Check if session has expired
        if datetime.utcnow() - self.users[username].last_login > self.session_expiry:
            del self.session_tokens[session_token]
            return None
            
        self.users[username].last_login = datetime.utcnow()
        return username

    def _hash_password(self, password: str, salt: str) -> str:
        """Securely hash a password using PBKDF2."""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # High iteration count for security
        ).hex()

    def _verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify a password against its stored hash."""
        return hmac.compare_digest(
            self._hash_password(password, salt),
            stored_hash
        )

    def logout(self, session_token: str) -> None:
        """Invalidate a session token."""
        if session_token in self.session_tokens:
            del self.session_tokens[session_token]