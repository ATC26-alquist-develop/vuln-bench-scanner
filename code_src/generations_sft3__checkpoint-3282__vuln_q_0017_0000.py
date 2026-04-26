import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from http import cookies
import secrets
import hashlib
from functools import wraps

class SecureSession:
    def __init__(self, secret_key: str):
        # Use a secure random key for HMAC
        self.secret_key = secret_key.encode('utf-8')
        self.sessions: Dict[str, Dict] = {}
        
    def _generate_session_id(self) -> str:
        """Generate cryptographically secure random session ID"""
        return secrets.token_urlsafe(32)
    
    def _create_session(self, user_id: str) -> str:
        """Create new session with secure attributes"""
        session_id = self._generate_session_id()
        expiration = datetime.utcnow() + timedelta(hours=1)
        self.sessions[session_id] = {
            'user_id': user_id,
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
        return session['user_id']
    
    def _sign_session(self, session_id: str) -> str:
        """Create HMAC signature for session ID"""
        return hashlib.sha256(self.secret_key + session_id).hexdigest()
    
    def create_session(self, user_id: str) -> str:
        """Create new session for authenticated user"""
        session_id = self._generate_session_id()
        self.sessions[session_id] = {
            'user_id': user_id,
            'expiration': datetime.utcnow() + timedelta(hours=1)
        }
        return session_id
    
    def validate_session(self, session_id: str, cookie: Optional[cookies.SimpleCookie] = None) -> Optional[str]:
        """Validate session using secure methods"""
        if cookie:
            try:
                signature = cookie['session'].value.split(':')[0]
                session_id = cookie['session'].value.split(':')[1]
            except (KeyError, IndexError):
                return None
        else:
            signature = None
            session_id = session_id
        
        if not signature or not self._verify_session(session_id):
            return None
        
        if not signature or not self._sign_session(session_id):
            return None
        
        return self._verify_session(session_id)

def secure_session_middleware(app):
    """Secure session middleware for web applications"""
    @app.middleware('request')
    async def secure_session(request):
        session_id = request.cookies.get('session')
        if not session_id:
            return
        
        session = app['session_manager'].validate_session(session_id)
        if session:
            request.session = session
        else:
            request.session = None

def login_required(func):
    """Decorator to protect routes with login required"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session:
            return {'error': 'Unauthorized'}, 401
        return func(request, *args, **kwargs)
    return wrapper