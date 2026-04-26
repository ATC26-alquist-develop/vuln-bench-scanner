import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from http import cookies
import secrets
import hashlib
import time

class SecureLoginSystem:
    def __init__(self, session_duration: int = 3600):
        self.sessions: Dict[str, Dict] = {}
        self.session_duration = session_duration

    def _generate_secure_token(self) -> str:
        """Generate cryptographically secure random token."""
        return secrets.token_hex(32)

    def _hash_password(self, password: str) -> str:
        """Securely hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and create session."""
        # In a real system, validate username and password against database
        # This is a simplified example
        if username == "admin" and self._hash_password(password) == "hashed_admin_password":
            session_token = self._generate_secure_token()
            expiration = datetime.now() + timedelta(seconds=self.session_duration)
            self.sessions[session_token] = {
                "username": username,
                "expiration": expiration
            }
            return session_token
        return None

    def logout(self, session_token: str) -> None:
        """Remove user session."""
        self.sessions.pop(session_token, None)

    def is_session_valid(self, session_token: str) -> bool:
        """Check if session is valid and not expired."""
        if session_token not in self.sessions:
            return False
        
        session = self.sessions[session_token]
        if datetime.now() > session["expiration"]:
            self.logout(session_token)
            return False
        
        return True

    def get_user_from_session(self, session_token: str) -> Optional[str]:
        """Get username from valid session."""
        if not self.is_session_valid(session_token):
            return None
        
        return self.sessions[session_token]["username"]

    def create_secure_cookie(self, session_token: str) -> cookies.SimpleCookie:
        """Create secure HTTP-only cookie."""
        cookie = cookies.SimpleCookie()
        cookie["session"] = session_token
        cookie["session"]["httponly"] = True
        cookie["session"]["secure"] = True
        cookie["session"]["max-age"] = self.session_duration
        cookie["session"]["path"] = "/"
        return cookie

    def read_secure_cookie(self, cookie_string: str) -> Optional[str]:
        """Read secure cookie."""
        cookie = cookies.SimpleCookie(cookie_string)
        if "session" in cookie:
            return cookie["session"].value
        return None