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
        self.cookie_domain = None  # Set in init to allow customization

    def set_cookie(self, response, user_id: str) -> None:
        """Set secure cookie with user ID."""
        if not user_id or len(user_id) > 64:
            raise ValueError("Invalid user ID")

        # Generate secure random value
        secure_value = secrets.token_hex(32)
        
        # Set secure cookie options
        cookie = http.cookies.SimpleCookie()
        cookie[self.cookie_name] = secure_value
        cookie[self.cookie_name]['httponly'] = True
        cookie[self.cookie_name]['secure'] = True
        cookie[self.cookie_name]['samesite'] = 'Strict'
        cookie[self.cookie_name]['max-age'] = 3600  # 1 hour
        cookie[self.cookie_name]['path'] = '/'
        
        # Set secure domain if provided
        if self.cookie_domain:
            cookie[self.cookie_name]['domain'] = self.cookie_domain
            
        # Set secure flags
        cookie[self.cookie_name]['expires'] = (datetime.utcnow() + timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        cookie[self.cookie_name]['version'] = 1
        
        response.set_cookie(self.cookie_name, secure_value, **cookie[self.cookie_name])

    def get_cookie(self, request) -> Optional[str]:
        """Get secure cookie value."""
        if not request:
            return None
            
        cookie = http.cookies.SimpleCookie(request.COOKIES)
        if self.cookie_name not in cookie:
            return None
            
        # Verify cookie hasn't been tampered with
        try:
            cookie[self.cookie_name].decode('utf-8')
        except UnicodeDecodeError:
            return None
            
        # Verify cookie hasn't expired
        if datetime.utcnow() > datetime.strptime(cookie[self.cookie_name]['expires'], '%a, %d %b %Y %H:%M:%S GMT'):
            return None
            
        return cookie[self.cookie_name].value

    def cleanup_expired_cookies(self, request) -> None:
        """Remove expired cookies."""
        if not request:
            return
            
        cookie = http.cookies.SimpleCookie(request.COOKIES)
        for name in list(cookie):
            if name.startswith(self.cookie_name):
                cookie[name]['expires'] = (datetime.utcnow() - timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT')
                cookie[name].max_age = 0
                cookie[name].path = '/'
                cookie[name].domain = self.cookie_domain
        request.COOKIES = cookie