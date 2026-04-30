import secrets
import re
from urllib.parse import urlparse, urlunparse
from typing import Dict, Optional
import hmac
import hashlib
import time

class SecureURLShortener:
    def __init__(self, max_length: int = 2048, expiration: int = 3600):
        self.max_length = max_length
        self.expiration = expiration
        self.url_map: Dict[str, tuple] = {}
        self.secret_key = secrets.token_bytes(32)  # Secure secret key generation

    def _generate_short_code(self) -> str:
        """Generate a cryptographically secure random short code."""
        return secrets.token_urlsafe(16)[:16]  # 16 chars for URL safety

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format and scheme."""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except ValueError:
            return False

    def _hash_key(self, key: str) -> str:
        """Create a secure hash of the key."""
        return hmac.new(self.secret_key, key.encode(), hashlib.sha256).hexdigest()

    def shorten_url(self, long_url: str) -> Optional[str]:
        """Shorten a URL with security checks."""
        if not self._is_valid_url(long_url):
            return None

        if len(long_url) > self.max_length:
            return None

        short_code = self._generate_short_code()
        hashed_key = self._hash_key(short_code)

        if hashed_key in self.url_map:
            return None  # Collision detected, try again

        expiration_time = int(time.time()) + self.expiration
        self.url_map[hashed_key] = (long_url, expiration_time)
        return short_code

    def redirect_url(self, short_code: str) -> Optional[str]:
        """Redirect to original URL if valid and not expired."""
        hashed_key = self._hash_key(short_code)
        if hashed_key in self.url_map:
            long_url, expiration_time = self.url_map[hashed_key]
            if int(time.time()) < expiration_time:
                return long_url
            else:
                del self.url_map[hashed_key]  # Remove expired URL
        return None

    def cleanup_expired_urls(self):
        """Remove expired URLs from the map."""
        current_time = int(time.time())
        expired_keys = [key for key, (_, exp_time) in self.url_map.items() if current_time >= exp_time]
        for key in expired_keys:
            del self.url_map[key]