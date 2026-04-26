import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from http import cookies
import secrets
import hashlib
import time

class SecureLoginSystem:
    def __init__(self, secret_key: str):
        # Use a secure random number generator for secret key
        self._secret_key = secrets.token_bytes(32)
        self._session_duration = timedelta(minutes=30)
        self._sessions: Dict[str, Dict] = {}
        
    def _generate_session_id(self) -> str:
        """Generate cryptographically secure session ID."""
        return secrets.token_urlsafe(32)
    
    def _hash_password(self, password: str) -> str:
        """Securely hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and create session."""
        # In a real system, validate against database
        if self._hash_password(password) != "hashed_password":  # Replace with actual hash
            return None
            
        session_id = self._generate_session_id()
        expiration = datetime.now() + self._session_duration
        
        self._sessions[session_id] = {
            'username': username,
            'expiration': expiration
        }
        
        return session_id
    
    def logout(self, session_id: str) -> None:
        """Remove session."""
        self._sessions.pop(session_id, None)
    
    def is_session_valid(self, session_id: str) -> bool:
        """Check if session is valid and not expired."""
        if session_id not in self._sessions:
            return False
            
        session = self._sessions[session_id]
        if datetime.now() > session['expiration']:
            self.logout(session_id)
            return False
            
        return True
    
    def get_username(self, session_id: str) -> Optional[str]:
        """Get username from valid session."""
        if not self.is_session_valid(session_id):
            return None
            
        return self._sessions[session_id]['username']
    
    def create_secure_cookie(self, session_id: str) -> cookies.SimpleCookie:
        """Create secure HTTP-only cookie."""
        if not self.is_session_valid(session_id):
            return None
            
        cookie = cookies.SimpleCookie()
        cookie['session_id'] = session_id
        cookie['session_id']['httponly'] = True
        cookie['session_id']['secure'] = True
        cookie['session_id']['samesite'] = 'Strict'
        cookie['session_id']['max-age'] = int(self._session_duration.total_seconds())
        cookie['session_id']['path'] = '/'
        
        return cookie
    
    def parse_secure_cookie(self, cookie_string: str) -> Optional[str]:
        """Parse secure cookie."""
        cookie = cookies.SimpleCookie(cookie_string)
        session_id = cookie.get('session_id')
        if session_id and session_id.value:
            return session_id.value
        return None