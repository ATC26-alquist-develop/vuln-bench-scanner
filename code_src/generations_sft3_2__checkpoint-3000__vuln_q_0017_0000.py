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

def secure_cookie_handler(response, session_manager: SecureSessionManager):
    """Secure cookie handler for session management"""
    session_id = response.cookies.get('session_id')
    if session_id:
        session_manager.validate_session(session_id)
    else:
        session_id = session_manager.create_session('guest')
        response.set_cookie(
            'session_id',
            session_id,
            max_age=int(session_manager.session_duration.total_seconds()),
            httponly=True,
            secure=True,
            samesite='Strict'
        )

def login_required(func):
    """Decorator to protect routes requiring authentication"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return {'error': 'Unauthorized'}, 401
        
        username = session_manager.validate_session(session_id)
        if not username:
            return {'error': 'Invalid session'}, 401
            
        return func(request, username, *args, **kwargs)
    return wrapper

# Usage example
session_manager = SecureSessionManager('your-secret-key-here')