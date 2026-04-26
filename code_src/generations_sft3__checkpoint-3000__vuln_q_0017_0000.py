```python
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from http import cookies
import secrets
import hashlib
from functools import wraps

class SecureSessionManager:
    def __init__(self, secret_key: str, session_duration: int = 3600):
        # Use a secure random key for HMAC
        self.secret_key = secret_key.encode('utf-8')
        self.session_duration = timedelta(seconds=session_duration)
        self.sessions: Dict[str, Dict] = {}

    def _generate_session_id(self) -> str:
        """Generate cryptographically secure random session ID"""
        return secrets.token_urlsafe(32)

    def _create_session(self, username: str) -> str:
        """Create new session with secure token"""
        session_id = self._generate_session_id()
        expiration = datetime.utcnow() + self.session_duration
        self.sessions[session_id] = {
            'username': username,
            'expiration': expiration
        }
        return session_id

    def _validate_session(self, session_id: str) -> Optional[str]:
        """Validate session exists and hasn't expired"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        if datetime.utcnow() > session['expiration']:
            del self.sessions[session_id]
            return None
        return session['username']

    def create_session(self, username: str) -> str:
        """Create new session for authenticated user"""
        session_id = self._create_session(username)
        return session_id

    def validate_session(self, session_id: str) -> Optional[str]:
        """Validate session and return username if valid"""
        return self._validate_session(session_id)

    def delete_session(self, session_id: str) -> None:
        """Delete session"""
        if session_id in self.sessions:
            del self.sessions[session_id]

def secure_cookie_handler(request, response):
    """Secure cookie handling middleware"""
    if 'HTTP_COOKIE' in request.headers:
        cookies = cookies.SimpleCookie(request.headers['HTTP_COOKIE'])
        session_id = cookies.get('session_id')
        if session_id:
            session_manager = request.context.get('session_manager')
            if session_manager:
                username = session_manager.validate_session(session_id.value)
                if username:
                    response.set_cookie(
                        'session_id',
                        session_id.value,
                        max_age=3600,
                        httponly=True,
                        secure=True,
                        samesite='Strict'
                    )
                else:
                    response.set_cookie(
                        'session_id',
                        '',
                        max_age=0,
                        httponly=True,
                        secure=True,
                        samesite='Strict'
                    )

def hash_password(password: str) -> str:
    """Securely hash password using Argon2"""
    # In a real implementation, use a proper password hashing library like Argon2
    # This is a placeholder for demonstration purposes
    salt = secrets.token_bytes(16)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

def create_session_manager(secret_key: str) -> SecureSessionManager:
    """Create a new session manager with secure defaults"""
    return SecureSessionManager(secret_key)

# Example usage
def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        session_manager = request.context.get('session_manager')
        if not session_manager:
            return "Unauthorized", 401
        
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            return "Unauthorized", 401
            
        username = session_manager.validate_session(session_id)
        if not username:
            return "Unauthorized", 401
            
        return func(request, username, *args, **kwargs)
    return wrapper