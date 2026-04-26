```python
import secrets
import time
from typing import Dict, Optional
from http import cookies
import hashlib
import hmac
import base64

class SecureSessionManager:
    def __init__(self, secret_key: bytes, session_duration: int = 3600):
        """
        Initialize secure session manager with proper security controls.
        
        Args:
            secret_key: A secure random key for HMAC
            session_duration: Maximum session lifetime in seconds
        """
        self.secret_key = secret_key
        self.session_duration = session_duration
        self.sessions: Dict[str, Dict] = {}
        
    def create_session(self, username: str) -> str:
        """
        Create a new secure session.
        
        Args:
            username: User identifier
        
        Returns:
            Secure session token
        """
        if not username or not isinstance(username, str):
            raise ValueError("Invalid username")
            
        # Generate secure random token
        session_id = secrets.token_hex(32)
        
        # Create secure session data
        session_data = {
            'username': username,
            'created_at': int(time.time()),
            'last_activity': int(time.time())
        }
        
        # Store session data
        self.sessions[session_id] = session_data
        
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[str]:
        """
        Validate session and update last activity.
        
        Args:
            session_id: Session token to validate
            
        Returns:
            Validated username or None if invalid
        """
        if not session_id or not isinstance(session_id, str):
            return None
            
        session = self.sessions.get(session_id)
        if not session:
            return None
            
        # Check session expiration
        if int(time.time()) - session['last_activity'] > self.session_duration:
            del self.sessions[session_id]
            return None
            
        # Update last activity
        session['last_activity'] = int(time.time())
        
        return session['username']
    
    def generate_secure_cookie(self, session_id: str) -> str:
        """
        Generate secure HTTP-only cookie.
        
        Args:
            session_id: Session token to encode
            
        Returns:
            Secure cookie string
        """
        if not session_id or not isinstance(session_id, str):
            raise ValueError("Invalid session ID")
            
        # Create secure signature
        signature = hmac.new(
            self.secret_key,
            session_id.encode(),
            hashlib.sha256
        ).digest()
        
        # Encode and URL-escape
        encoded_signature = base64.urlsafe_b64encode(signature).decode()
        encoded_session_id = base64.urlsafe_b64encode(session_id.encode()).decode()
        
        # Create secure cookie
        cookie = cookies.SimpleCookie()
        cookie['session'] = f"{encoded_session_id}.{encoded_signature}"
        cookie['session']['httponly'] = True
        cookie['session']['secure'] = True
        cookie['session']['samesite'] = 'Strict'
        cookie['session']['max-age'] = self.session_duration
        
        return cookie.output().strip()
    
    def parse_secure_cookie(self, cookie_string: str) -> Optional[str]:
        """
        Parse secure HTTP-only cookie.
        
        Args:
            cookie_string: Cookie string to parse
            
        Returns:
            Validated session ID or None if invalid
        """
        if not cookie_string or not isinstance(cookie_string, str):
            return None
            
        try:
            cookie = cookies.SimpleCookie(cookie_string)
            if 'session' not in cookie:
                return None
                
            session = cookie['session'].value
            if not session:
                return None
                
            # Decode and verify signature
            encoded_session_id, encoded_signature = session.split('.')
            decoded_signature = base64.urlsafe_b64decode(encoded_signature)
            decoded_session_id =