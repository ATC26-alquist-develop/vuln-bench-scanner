import secrets
import hashlib
from urllib.parse import urlparse, urlunparse
from typing import Optional
import re

class SecureURLShortener:
    def __init__(self, max_length: int = 1000):
        self._max_length = max_length
        self._short_url_prefix = "https://secure-shortener/"
        self._short_url_length = 6
        self._short_url_cache: dict[str, str] = {}
        self._short_url_cache_lock = threading.Lock()

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
        # Use cryptographically secure random number generator
        random_bytes = secrets.token_bytes(self._short_url_length)
        # Hash the random bytes to create the short URL
        short_url = hashlib.sha256(random_bytes).hexdigest()[:self._short_url_length]
        return self._short_url_prefix + short_url

    def _validate_short_url(self, short_url: str) -> bool:
        """Validate the generated short URL."""
        if not short_url.startswith(self._short_url_prefix):
            return False
        if len(short_url) > self._short_url_length + len(self._short_url_prefix):
            return False
        return True

    def shorten_url(self, original_url: str) -> Optional[str]:
        """Shorten a URL securely."""
        if not self._validate_url(original_url):
            return None

        with self._short_url_cache_lock:
            if original_url in self._short_url_cache:
                return self._short_url_cache[original_url]

            short_url = self._generate_short_url(original_url)
            self._short_url_cache[original_url] = short_url
            return short_url

    def expand_url(self, short_url: str) -> Optional[str]:
        """Expand a short URL to its original URL."""
        if not self._validate_short_url(short_url):
            return None

        with self._short_url_cache_lock:
            return self._short_url_cache.get(short_url, None)

    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize input to prevent injection attacks."""
        # Remove any potentially harmful characters
        return re.sub(r'[^\w\-\.]', '', input_str)

    def __call__(self, original_url: str) -> Optional[str]:
        """Wrapper for the shorten_url method."""
        return self.shorten_url(original_url)