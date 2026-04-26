import secrets
import hashlib
from urllib.parse import urlparse, urlunparse
from typing import Optional
import re

class SecureURLShortener:
    def __init__(self, max_length: int = 1000):
        self.max_length = max_length
        self._short_url_prefix = "https://secure-shortener/"
        self._url_map: dict[str, str] = {}
        self._short_url_counter = 0

    def _validate_url(self, url: str) -> bool:
        """Validate URL format and length."""
        if not url or len(url) > self.max_length:
            return False
        
        # Basic URL format validation
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def _generate_short_url(self) -> str:
        """Generate a secure random short URL."""
        while True:
            # Generate a cryptographically secure random string
            random_string = secrets.token_hex(16)
            # Create a hash of the random string
            hash_object = hashlib.sha256(random_string.encode())
            # Use the first 6 characters of the hash as the short URL
            short_url = self._short_url_prefix + hash_object.hexdigest()[:6]
            # Check if the short URL is already in use
            if short_url not in self._url_map:
                return short_url

    def shorten_url(self, long_url: str) -> Optional[str]:
        """Shorten a URL with security measures."""
        if not self._validate_url(long_url):
            return None

        try:
            # Sanitize the URL
            sanitized_url = re.sub(r'[^\w\-\.]', '', long_url)
            
            # Generate a new short URL
            short_url = self._generate_short_url()
            
            # Store the mapping
            self._url_map[short_url] = sanitized_url
            
            return short_url
        except Exception:
            return None

    def get_long_url(self, short_url: str) -> Optional[str]:
        """Retrieve the original URL from a short URL."""
        if not self._validate_url(short_url):
            return None
            
        return self._url_map.get(short_url)

    def __del__(self):
        """Clean up any resources."""
        self._url_map.clear()