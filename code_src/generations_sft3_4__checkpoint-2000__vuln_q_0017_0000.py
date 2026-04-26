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
        return hashlib.argon2.using(salt_length=16).hash(password)

    def _verify_password(self, stored_hash: str, provided_password: str) -> bool:
        """Securely verify password against stored hash."""
        # In production, use a proper password verification method
        return hashlib.argon2.verify(provided_password, stored_hash)

    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and create session."""
        # In production, fetch user from secure database
        if not username or not password:
            return None
            
        # In production, validate and sanitize inputs
        if not self._verify_password(username, password):
            return None

        session_id = self._generate_session_id()
        expiration = datetime.utcnow() + self._session_duration
        self._sessions[session_id] = {
            'username': username,
            'expiration': expiration
        }
        return session_id

    def logout(self, session_id: str) -> None:
        """Invalidate user session."""
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
        if not self.is_session_valid(session_id):
            return None
        return self._sessions[session_id]['username']

    def create_secure_cookie(self, session_id: str) -> str:
        """Create secure HTTP-only cookie."""
        if not self.is_session_valid(session_id):
            raise ValueError("Invalid session ID")
            
        cookie = cookies.SimpleCookie()
        cookie['session'] = session_id
        cookie['session']['httponly'] = True
        cookie['session']['secure'] = True
        cookie['session']['max-age'] = int(self._session_duration.total_seconds())
        cookie['session']['path'] = '/'
        return cookie.output()

    def parse_secure_cookie(self, cookie_string: str) -> Optional[str]:
        """Parse secure HTTP-only cookie."""
        cookie = cookies.SimpleCookie(cookie_string)
        if 'session' not in cookie:
            return None
        session_id = cookie['session'].value
        if not self.is_session_valid(session_id):
            del cookie['session']
            return None
        return session_id