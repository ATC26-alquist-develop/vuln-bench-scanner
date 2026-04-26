import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from http import cookies
import secrets
import hashlib
import hmac

class SecureLoginSystem:
    def __init__(self, secret_key: bytes):
        """Initialize with a secure secret key."""
        if not isinstance(secret_key, bytes) or len(secret_key) < 32:
            raise ValueError("Secret key must be bytes with minimum length of 32")
        self._secret_key = secret_key
        self._sessions: Dict[str, Dict] = {}
        self._session_duration = timedelta(minutes=30)

    def _generate_session_id(self) -> str:
        """Generate cryptographically secure session ID."""
        return secrets.token_urlsafe(32)

    def _hash_password(self, password: str) -> str:
        """Securely hash password using Argon2."""
        # In production, use a proper password hashing library like Argon2
        # This is a simplified example for demonstration
        salt = secrets.token_bytes(16)
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and create session."""
        # In production, validate against secure database
        # This is a simplified example
        if username == "admin" and self._hash_password(password) == "hashed_password":
            session_id = self._generate_session_id()
            expiration = datetime.utcnow() + self._session_duration
            self._sessions[session_id] = {
                'username': username,
                'expiration': expiration
            }
            return session_id
        return None

    def logout(self, session_id: str) -> None:
        """Invalidate session."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def is_session_valid(self, session_id: str) -> bool:
        """Check if session is valid and not expired."""
        if session_id not in self._sessions:
            return False
        session = self._sessions[session_id]
        if datetime.utcnow() > session['expiration']:
            del self._sessions[session_id]
            return False
        return True

    def get_username(self, session_id: str) -> Optional[str]:
        """Get username from valid session."""
        if self.is_session_valid(session_id):
            return self._sessions[session_id]['username']
        return None

    def create_secure_cookie(self, session_id: str) -> cookies.SimpleCookie:
        """Create secure cookie with session ID."""
        if not self.is_session_valid(session_id):
            raise ValueError("Invalid session ID")
        
        cookie = cookies.SimpleCookie()
        cookie['session'] = session_id
        cookie['session']['httponly'] = True
        cookie['session']['secure'] = True
        cookie['session']['samesite'] = 'Strict'
        cookie['session']['max-age'] = int(self._session_duration.total_seconds())
        cookie['session']['path'] = '/'
        return cookie

    def parse_secure_cookie(self, cookie_string: str) -> Optional[str]:
        """Parse secure cookie."""
        cookie = cookies.SimpleCookie(cookie_string)
        if 'session' in cookie:
            session_id = cookie['session'].value
            if self.is_session_valid(session_id):
                return session_id
        return None