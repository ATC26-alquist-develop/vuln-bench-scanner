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
        """Sign session ID for secure transmission"""
        if session_id not in self.sessions:
            raise ValueError("Invalid session ID")
        return hashlib.sha256(session_id.encode('utf-8')).hexdigest()
    
    def _verify_signature(self, session_id: str) -> bool:
        """Verify session ID signature"""
        try:
            session_id = self._sign_session(session_id)
            return secrets.compare_digest(session_id, session_id)
        except ValueError:
            return False

def login_required(func):
    """Decorator to protect routes requiring authentication"""
    @wraps(func)
    def wrapper(session: SecureSession, *args, **kwargs):
        cookie = request.cookies.get('session_id')
        if not cookie or not session._verify_signature(cookie):
            return "Unauthorized", 401
        return func(session, *args, **kwargs)
    return wrapper

# Usage example
class SecureLogin:
    def __init__(self, secret_key: str):
        self.session = SecureSession(secret_key)
    
    def login(self, user_id: str) -> str:
        """Create new session for authenticated user"""
        session_id = self.session._create_session(user_id)
        return session_id
    
    def logout(self, session: SecureSession) -> None:
        """Remove user session"""
        session.sessions.pop(session._sign_session(session._generate_session_id()), None)
    
    def create_cookie(self, session_id: str) -> str:
        """Create secure HTTP-only cookie"""
        cookie = cookies.SimpleCookie()
        cookie['session_id'] = session_id
        cookie['session_id']['httponly'] = True
        cookie['session_id']['secure'] = True
        cookie['session_id']['max-age'] = 3600
        cookie['session_id']['path'] = '/'
        return cookie.output()

# Usage
login_system = SecureLogin('your-secret-key-here')