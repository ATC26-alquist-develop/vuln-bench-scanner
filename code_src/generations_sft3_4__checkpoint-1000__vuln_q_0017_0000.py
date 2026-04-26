import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from http import cookies
import secrets
import hashlib
import time

class SecureSessionManager:
    def __init__(self, secret_key: str, session_duration: int = 3600):
        """
        Initialize secure session manager with proper security controls.
        
        Args:
            secret_key: A secure random key for HMAC
            session_duration: Maximum session lifetime in seconds
        """
        self.secret_key = secret_key.encode('utf-8')
        self.session_duration = session_duration
        self.sessions: Dict[str, Dict] = {}

    def create_session(self, user_id: str) -> str:
        """
        Create a new secure session.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Secure session token
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user_id")
            
        # Generate secure random token
        session_token = secrets.token_hex(32)
        
        # Create secure session data
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(seconds=self.session_duration)).isoformat()
        }
        
        # Create secure cookie
        secure_cookie = cookies.SimpleCookie()
        secure_cookie['session'] = session_token
        secure_cookie['session']['httponly'] = True
        secure_cookie['session']['secure'] = True
        secure_cookie['session']['samesite'] = 'Strict'
        secure_cookie['session']['max-age'] = self.session_duration
        secure_cookie['session']['path'] = '/'
        
        # Store session data
        self.sessions[session_token] = session_data
        
        return session_token

    def validate_session(self, session_token: str) -> Optional[str]:
        """
        Validate a session token.
        
        Args:
            session_token: The session token to validate
            
        Returns:
            User ID if valid, None otherwise
        """
        if not session_token or not isinstance(session_token, str):
            return None
            
        session = self.sessions.get(session_token)
        if not session:
            return None
            
        # Check if session has expired
        if datetime.fromisoformat(session['expires_at']) < datetime.utcnow():
            del self.sessions[session_token]
            return None
            
        return session['user_id']

    def cleanup_expired_sessions(self):
        """
        Remove expired sessions from the cache.
        """
        current_time = datetime.utcnow()
        expired_tokens = [
            token for token, session in self.sessions.items()
            if current_time > datetime.fromisoformat(session['expires_at'])
        ]
        for token in expired_tokens:
            del self.sessions[token]

    def logout(self, session_token: str) -> None:
        """
        Invalidate a session token.
        
        Args:
            session_token: The session token to invalidate
        """
        if session_token in self.sessions:
            del self.sessions[session_token]

# Example usage
if __name__ == "__main__":
    # Initialize with a secure random key
    session_manager = SecureSessionManager(secrets.token_hex(32))
    
    # Create a new session
    user_id = "user123"
    session_token = session_manager.create_session(user_id)
    print(f"Session created: {session_token}")
    
    # Validate session
    validated_user = session_manager.validate_session(session_token)
    print(f"Validated user: {validated_user}")
    
    # Cleanup expired sessions
    session_manager.cleanup_expired_sessions()