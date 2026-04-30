import re
import hashlib
import secrets
from typing import Optional
from urllib.parse import urlparse
import time
from datetime import datetime, timedelta

class SecureURLShortener:
    def __init__(self):
        self.url_map = {}
        self.expiration_time = timedelta(hours=24)  # 24 hour expiration
        self.max_length = 2048  # Reasonable URL length limit
        self.max_urls = 1000000  # Reasonable limit on total URLs stored

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format and scheme."""
        try:
            result = urlparse(url)
            return all([
                result.scheme in ('http', 'https'),
                result.netloc,
                len(url) <= self.max_length
            ])
        except Exception:
            return False

    def _generate_short_code(self) -> str:
        """Generate a cryptographically secure random short code."""
        return hashlib.sha256(secrets.token_bytes(32)).hexdigest()[:8]

    def shorten_url(self, long_url: str) -> Optional[str]:
        """Shorten a long URL with security measures."""
        if not self._is_valid_url(long_url):
            return None

        if len(self.url_map) >= self.max_urls:
            return None

        short_code = self._generate_short_code()
        expiration = datetime.utcnow() + self.expiration_time

        self.url_map[short_code] = (long_url, expiration)
        return short_code

    def redirect_url(self, short_code: str) -> Optional[str]:
        """Redirect to original URL if valid and not expired."""
        if short_code not in self.url_map:
            return None

        long_url, expiration = self.url_map[short_code]
        if datetime.utcnow() > expiration:
            del self.url_map[short_code]
            return None

        return long_url

    def cleanup_expired(self):
        """Remove expired URLs from the map."""
        current_time = datetime.utcnow()
        expired_codes = [
            code for code, (_, exp) in self.url_map.items()
            if current_time > exp
        ]
        for code in expired_codes:
            del self.url_map[code]

# Usage example
if __name__ == "__main__":
    url_shortener = SecureURLShortener()
    
    # Shorten a URL
    long_url = "https://www.example.com/some/very/long/url/that/needs/to/be/shortened"
    short_code = url_shortener.shorten_url(long_url)
    if short_code:
        print(f"Shortened URL: {short_code}")
    else:
        print("Failed to shorten URL")

    # Redirect a shortened URL
    original_url = url_shortener.redirect_url(short_code)
    if original_url:
        print(f"Redirected to: {original_url}")
    else:
        print("Invalid or expired short URL")