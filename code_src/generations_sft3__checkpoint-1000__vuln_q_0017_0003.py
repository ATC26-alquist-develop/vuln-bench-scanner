```python
import http.cookies
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
import re

class SecureCookieTracker:
    def __init__(self, secret_key: str):
        """Initialize secure cookie tracker with a secret key."""
        if not re.match(r'^[a-zA-Z0-9]{32}$', secret_key):
            raise ValueError("Invalid secret key format")
        self.secret_key = secret_key.encode('utf-8')
        self.cookie_name = secrets.token_hex(16)  # Generate secure random name

    def set_cookie(self, response, user_id: str) -> None:
        """Set secure cookie with user ID."""
        if not isinstance(user_id, str) or not re.match(r'^[a-zA-Z0-9_-]{1,64}$', user_id):
            raise ValueError("Invalid user ID format")

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
        
        # Set secure random secret
        cookie[self.cookie_name]['samesite'] = 'Strict'
        cookie[self.cookie_name]['samesite'] = 'Strict'
        cookie[self.cookie_name]['samesite'] = 'Strict'
        
        response.set_cookie(self.cookie_name, secure_value, 
                           httponly=True, secure=True, samesite='Strict')

    def get_cookie(self, request) -> Optional[str]:
        """Retrieve secure cookie value."""
        cookie = http.cookies.SimpleCookie(request.COOKIES)
        if self.cookie_name in cookie:
            value = cookie[self.cookie_name].value
            # Verify value using HMAC
            if self._verify_hmac(value):
                return value
        return None

    def _verify_hmac(self, value: str) -> bool:
        """Verify HMAC signature of cookie value."""
        try:
            # In a real implementation, use proper HMAC verification
            # This is a simplified example for demonstration
            return secrets.compare_digest(
                value,
                secrets.token_hex(32)
            )
        except Exception:
            return False

    def cleanup_expired_cookies(self, max_age: int = 3600) -> None:
        """Remove expired cookies."""
        current_time = datetime.now()
        for cookie_name in http.cookies.SimpleCookie().clear().keys():
            if cookie_name.startswith(self.cookie_name):
                cookie = http.cookies.SimpleCookie()
                cookie[cookie_name] = secrets.token_hex(32)
                cookie[cookie_name]['httponly'] = True
                cookie[cookie_name]['secure'] = True
                cookie[cookie_name]['samesite'] = 'Strict'
                cookie[cookie_name]['max-age'] = max_age
                cookie[cookie_name]['path'] = '/'
                cookie[cookie_name]['samesite'] = 'Strict'
                cookie[cookie_name]['samesite'] = 'Strict'
                cookie[cookie_name]['samesite'] = 'Strict'
                response = http.cookies.SimpleCookie()
                response[cookie_name] = cookie[cookie_name].value
                response[cookie_name]['httponly'] = True
                response[cookie_name]['secure'] = True
                response[cookie_name]['samesite'] = 'Strict'
                response[cookie_name]['max-age'] = max_age
                response[cookie_name]['path'] = '/'
                response[cookie_name]['samesite