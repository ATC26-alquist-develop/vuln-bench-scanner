```python
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from http import cookies
import secrets
import hashlib
import hmac
from functools import wraps

class SecureLoginSystem:
    def __init__(self, secret_key: bytes, session_duration: int = 3600):
        # Use a cryptographically secure random key
        self.secret_key = secret_key
        # Session duration in seconds
        self.session_duration = timedelta(seconds=session_duration)
        
        # In-memory storage for simplicity, use proper database in production
        self.sessions: Dict[str, Dict] = {}
        
    def _generate_session_id(self) -> str:
        """Generate cryptographically secure session ID"""
        return secrets.token_urlsafe(32)
    
    def _hash_password(self, password: str) -> str:
        """Securely hash password using Argon2"""
        # In production, use a proper password hashing library like Argon2
        return hashlib.argon2.using(salt_size=16).hash(password)
    
    def _verify_password(self, stored_hash: str, provided_password: str) -> bool:
        """Securely verify password"""
        # In production, use a proper password verification method
        return hashlib.argon2.verify(provided_password, stored_hash)
    
    def _generate_secure_cookie(self, data: Dict) -> cookies.SimpleCookie:
        """Generate secure cookie with expiration"""
        secure_cookie = cookies.SimpleCookie()
        expiration = datetime.utcnow() + self.session_duration
        secure_cookie['session'] = hmac.new(
            self.secret_key,
            data['session_id'].encode(),
            hashlib.sha256
        ).hexdigest()
        secure_cookie['session']['expires'] = expiration.strftime('%a, %d %b %Y %H:%M:%S GMT')
        secure_cookie['session']['httponly'] = True
        secure_cookie['session']['secure'] = True
        return secure_cookie
    
    def register_user(self, username: str, password: str) -> bool:
        """Register new user with secure password hashing"""
        if not username or not password:
            return False
        # In production, use proper database with input validation
        session_id = self._generate_session_id()
        self.sessions[session_id] = {
            'username': username,
            'created_at': datetime.utcnow()
        }
        return True
    
    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and create session"""
        for session_id, session_data in self.sessions.items():
            if self._verify_password(session_data['username'], username) and \
               self._verify_password(session_data['password'], password):
                return session_id
        return None
    
    def logout(self, session_id: str) -> None:
        """Invalidate user session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def create_session_cookie(self, session_id: str) -> cookies.SimpleCookie:
        """Create secure session cookie"""
        if session_id not in self.sessions:
            return None
        return self._generate_secure_cookie({
            'session_id': session_id
        })
    
    def validate_session(self, cookie: Optional[cookies.SimpleCookie]) -> Optional[str]:
        """Validate session cookie"""
        if not cookie:
            return None
        session_id = cookie.get('session')
        if not session_id:
            return None
        # Verify HMAC
        try:
            session_data = hmac.new(
                self.secret_key,
                session_id.encode(),
                hashlib.sha256
            ).hexdigest()
            if session_data != cookie['session'].value:
                return None
            # Check expiration
            expiration = datetime.utcnow() - timedelta(seconds=1)
            if cookie['session']['expires'] < expiration:
                return None