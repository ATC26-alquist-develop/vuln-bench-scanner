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
            raise ValueError("Invalid user ID length")
            
        # Generate secure random value
        secure_value = secrets.token_hex(32)
        
        # Set secure cookie with expiration
        cookie = http.cookies.SimpleCookie()
        cookie[self.cookie_name] = secure_value
        cookie[self.cookie_name]['httponly'] = True
        cookie[self.cookie_name]['secure'] = True
        cookie[self.cookie_name]['samesite'] = 'Strict'
        cookie[self.cookie_name]['max-age'] = 3600  # 1 hour
        
        # Set secure domain if provided
        if self.cookie_domain:
            cookie[self.cookie_name]['domain'] = self.cookie_domain
            
        response.set_cookie(self.cookie_name, secure_value, 
                           httponly=True, secure=True, samesite='Strict',
                           max_age=3600, path='/')
        
    def get_cookie(self, request) -> Optional[str]:
        """Get secure cookie value."""
        if not request:
            return None
            
        cookie = http.cookies.SimpleCookie(request.COOKIES)
        if self.cookie_name in cookie:
            value = cookie[self.cookie_name].value
            # Verify value using HMAC
            if self._verify_hmac(value):
                return value
        return None

    def _verify_hmac(self, value: str) -> bool:
        """Verify HMAC of cookie value."""
        try:
            # Use constant-time comparison to prevent timing attacks
            return secrets.compare_digest(
                value,
                secrets.hmac(self.secret_key, value).hex()
            )
        except Exception:
            return False

    def cleanup_expired_cookies(self, current_time: float) -> None:
        """Remove expired cookies."""
        if not hasattr(self, 'cookie_domain'):
            return
            
        # Remove expired cookies
        expired = [c for c in http.cookies.SimpleCookie() 
                  if c['domain'] == self.cookie_domain and 
                  current_time - int(c['max-age']) > 0]
        for cookie in expired:
            del cookie

    def set_cookie_domain(self, domain: str) -> None:
        """Set secure cookie domain."""
        if not domain or not isinstance(domain, str):
            raise ValueError("Invalid domain")
        self.cookie_domain = domain

# Example usage
def setup_secure_tracker(secret_key: str) -> SecureCookieTracker:
    """Set up secure cookie tracker with secret key."""
    if not isinstance(secret_key, str):
        raise ValueError("Secret key must be a string")
    return SecureCookieTracker(secret_key)

# Usage example
if __name__ == "__main__":
    tracker = setup_secure_tracker("your-secret-key-here")
    tracker.set_cookie_domain("example.com")