import secrets
import hashlib
from urllib.parse import urlparse, urlunparse
from typing import Optional
import re

class SecureURLShortener:
    def __init__(self, max_length: int = 1000):
        self._max_length = max_length
        self._short_url_length = 6  # 6-character short URL
        self._short_url_prefix = "https://tinyurl.com/"
        self._short_url_map = {}
        self._allowed_chars = re.compile(r'^[a-zA-Z0-9\-\.]+$')

    def _validate_url(self, url: str) -> bool:
        """Validate URL format and length."""
        if not url or len(url) > self._max_length:
            return False
        
        try:
            result = urlparse(url)
            return all([result.scheme in ('http', 'https'), result.netloc])
        except Exception:
            return False

    def _generate_short_url(self, original_url: str) -> str:
        """Generate a secure random short URL."""
        if not self._validate_url(original_url):
            raise ValueError("Invalid URL format")

        # Generate a cryptographically secure random string
        random_string = secrets.token_hex(16)
        
        # Create hash of the original URL
        url_hash = hashlib.sha256(original_url.encode()).hexdigest()
        
        # Combine hash and random string
        combined = url_hash + random_string
        
        # Take first 6 characters as short URL
        short_url = combined[:self._short_url_length]
        
        # Ensure URL is valid
        if not self._allowed_chars.match(short_url):
            raise ValueError("Invalid URL format")
            
        return self._short_url_prefix + short_url

    def shorten(self, original_url: str) -> Optional[str]:
        """Shorten a URL."""
        if not self._validate_url(original_url):
            raise ValueError("Invalid URL format")

        if original_url in self._short_url_map:
            return self._short_url_map[original_url]

        short_url = self._generate_short_url(original_url)
        self._short_url_map[original_url] = short_url
        return short_url

    def expand(self, short_url: str) -> Optional[str]:
        """Expand a short URL to its original URL."""
        if not self._allowed_chars.match(short_url):
            raise ValueError("Invalid URL format")

        if short_url.startswith(self._short_url_prefix):
            original_url = short_url[len(self._short_url_prefix):]
            if original_url in self._short_url_map:
                return self._short_url_map[original_url]
        return None