import http.cookies
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
import time

class SecureCookieTracker:
    def __init__(self, secret_key: str):
        """Initialize secure cookie tracker with a secret key."""
        if not secret_key or len(secret_key) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        self.secret_key = secret_key.encode('utf-8')
        self.cookie_name = secrets.token_hex(16)  # Generate secure random name
        self.cookie_domain = None  # Set in constructor

    def set_cookie(self, response, user_id: str, domain: Optional[str] = None) -> None:
        """Set secure cookie with user ID."""
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user ID")
            
        if domain:
            self.cookie_domain = domain
            
        # Generate secure random value
        secure_value = secrets.token_hex(32)
        
        # Set secure cookie with expiration
        cookie = http.cookies.SimpleCookie()
        cookie[self.cookie_name] = secure_value
        cookie[self.cookie_name]['httponly'] = True
        cookie[self.cookie_name]['secure'] = True
        cookie[self.cookie_name]['samesite'] = 'Strict'
        cookie[self.cookie_name]['max-age'] = 3600  # 1 hour
        cookie[self.cookie_name]['path'] = '/'
        
        if self.cookie_domain:
            cookie[self.cookie_name]['domain'] = self.cookie_domain
            
        response.set_cookie(self.cookie_name, secure_value, **cookie[self.cookie_name])

    def get_user_id(self, request) -> Optional[str]:
        """Securely retrieve user ID from cookie."""
        if not request:
            return None
            
        cookie = http.cookies.SimpleCookie(request.COOKIES)
        if self.cookie_name not in cookie:
            return None
            
        value = cookie[self.cookie_name].value
        if not value:
            return None
            
        # Verify cookie hasn't been tampered with
        try:
            # Use constant-time comparison to prevent timing attacks
            if secrets.compare_digest(value, self._verify_cookie()):
                return value
        except Exception:
            pass
            
        return None

    def _verify_cookie(self) -> str:
        """Verify cookie integrity using HMAC."""
        timestamp = int(time.time())
        hmac = secrets.hmac(self.secret_key, f"{timestamp}{self.cookie_name}".encode('utf-8'))
        return hmac.hexdigest()

    def cleanup_expired_cookies(self, request) -> None:
        """Remove expired cookies."""
        cookie = http.cookies.SimpleCookie(request.COOKIES)
        if self.cookie_name not in cookie:
            return
            
        value = cookie[self.cookie_name].value
        if not value:
            return
            
        try:
            timestamp = int(time.time())
            if timestamp - int(value.split('.')[0]) > 3600:  # 1 hour
                cookie[self.cookie_name].expires = 0
                request.COOKIES[self.cookie_name] = cookie[self.cookie_name].OutputString()
        except Exception:
            pass