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
    
    def _verify_session(self, session_id: str) -> Optional[str]:
        """Verify session exists and hasn't expired"""
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
    
    def verify_session(self, session_id: str) -> Optional[str]:
        """Verify session and return username if valid"""
        return self._verify_session(session_id)
    
    def delete_session(self, session_id: str) -> None:
        """Delete session"""
        if session_id in self.sessions:
            del self.sessions[session_id]

def secure_cookie_response(response, session_id: str):
    """Add secure cookie to HTTP response"""
    cookie = cookies.SimpleCookie()
    cookie['session'] = session_id
    cookie['session']['httponly'] = True
    cookie['session']['secure'] = True
    cookie['session']['samesite'] = 'Strict'
    cookie['session']['max-age'] = int(3600)
    cookie['session']['path'] = '/'
    response.set_cookie(cookie['session'].coded_value, httponly=True)

def login_required(func):
    """Decorator to protect routes requiring authentication"""
    @wraps(func)
    def wrapper(session_manager, session_id, *args, **kwargs):
        username = session_manager.verify_session(session_id)
        if not username:
            return "Unauthorized", 401
        return func(session_manager, session_id, username, *args, **kwargs)
    return wrapper

# Usage example
secret_key = secrets.token_urlsafe(32)
session_manager = SecureSessionManager(secret_key)

def login_route(username: str, password: str) -> str:
    """Handle login"""
    # In real implementation, validate credentials against secure database
    if username == "admin" and password == "secure_password":
        session_id = session_manager.create_session(username)
        secure_cookie_response(response, session_id)
        return f"Login successful. Session ID: {session_id}"
    return "Invalid credentials", 401

@login_required(session_manager)
def protected_route(session_manager, session_id, username):
    """Protected route example"""
    return f"Welcome, {username}!"