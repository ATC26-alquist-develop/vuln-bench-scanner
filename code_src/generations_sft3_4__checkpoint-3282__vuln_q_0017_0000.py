```python
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
    
    def validate_session(self, cookie_value: str) -> Optional[str]:
        """Validate session using HMAC signature"""
        try:
            session_id = self._sign_session(cookie_value)
            return self._verify_session(session_id)
        except Exception:
            return None

class SecureLoginSystem:
    def __init__(self, secret_key: str):
        self.session_manager = SecureSession(secret_key)
        self.login_cookie_name = 'secure_session'
        
    def login(self, user_id: str) -> str:
        """Authenticate user and create session"""
        session_id = self.session_manager.create_session(user_id)
        return session_id
    
    def logout(self, session_id: str) -> None:
        """Invalidate user session"""
        if session_id:
            self.session_manager.sessions.pop(session_id, None)
    
    def create_secure_cookie(self, session_id: str) -> str:
        """Create secure HTTP-only session cookie"""
        cookie = cookies.SimpleCookie()
        cookie[self.login_cookie_name] = session_id
        cookie[self.login_cookie_name]['httponly'] = True
        cookie[self.login_cookie_name]['secure'] = True
        cookie[self.login_cookie_name]['max-age'] = 3600
        cookie[self.login_cookie_name]['path'] = '/'
        return cookie.toascii()

    def validate_session_cookie(self, cookie_value: str) -> Optional[str]:
        """Validate session using secure cookie"""
        return self.session_manager.validate_session(cookie_value)

# Usage example
if __name__ == "__main__":
    # Initialize with a strong secret key
    login_system = SecureLoginSystem('your-very-strong-secret-key-here')
    
    # Login
    user_id = "user123"
    session_id = login_system.login(user_id)
    
    # Create secure cookie
    secure_cookie = login_system.create_secure_cookie(session_id)
    
    # Validate session
    validated_user_id = login_system.validate_session_cookie(secure_cookie)
    if validated_user_id:
        print(f"Valid session for user: