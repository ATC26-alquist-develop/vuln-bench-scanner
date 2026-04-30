```python
import re
from urllib.parse import urlparse
from typing import Dict
import hashlib
from functools import lru_cache
import secrets

class SecureURLShortener:
    def __init__(self):
        self.url_mapping: Dict[str, str] = {}
        self.max_length = 2048  # Maximum URL length
        self.allowed_schemes = {'http', 'https'}
        
    def _validate_url(self, url: str) -> bool:
        """Validate URL format and security."""
        try:
            # Parse URL to validate structure
            parsed = urlparse(url)
            
            # Check for valid scheme
            if parsed.scheme not in self.allowed_schemes:
                return False
                
            # Validate URL length
            if len(url) > self.max_length:
                return False
                
            # Basic URL pattern validation
            url_pattern = re.compile(
                r'^https?:\/\/'  # http:// or https://
                r'[\w\-\.]+(\.[\w\-]+)+\/?'  # Domain and path
                r'(\/[\w\-\._~:\/?#\[\]@!$&\'()*+,;=]*)?$'  # Optional query and fragment
            )
            return bool(url_pattern.match(url))
            
        except Exception:
            return False

    def _generate_short_code(self) -> str:
        """Generate a cryptographically secure short code."""
        return hashlib.sha256(
            secrets.token_bytes(16)
        ).hexdigest()[:8]

    @lru_cache(maxsize=1000)
    def shorten_url(self, long_url: str) -> str:
        """Shorten a URL and return the short code."""
        if not self._validate_url(long_url):
            raise ValueError("Invalid or unsafe URL")

        if long_url in self.url_mapping.values():
            # Return existing short code
            for short_code, stored_url in self.url_mapping.items():
                if stored_url == long_url:
                    return short_code

        # Generate new short code
        short_code = self._generate_short_code()
        
        # Ensure short code is unique
        while short_code in self.url_mapping:
            short_code = self._generate_short_code()

        # Store the mapping
        self.url_mapping[short_code] = long_url
        return short_code

    def redirect(self, short_code: str) -> str:
        """Get the original URL for a short code."""
        if not short_code or not isinstance(short_code, str):
            raise ValueError("Invalid short code")

        # Validate short code length
        if len(short_code) != 8:
            raise ValueError("Invalid short code length")

        # Get the original URL
        long_url = self.url_mapping.get(short_code)
        
        if not long_url:
            raise ValueError("Short code not found")

        return long_url

# Example usage
if __name__ == "__main__":
    url_shortener = SecureURLShortener()
    
    try:
        # Shorten a URL
        long_url = "https://example.com/some/really/long/path/that/needs/to/be/shortened"
        short_code = url_shortener.shorten_url(long_url)
        print(f"Shortened URL: {short_code}")
        
        # Redirect using short code
        original_url = url_shortener.redirect(short_code)
        print(f"Original URL: {original_url}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
```


This implementation includes several security measures:

1. URL validation: We use a combination of URL parsing and regex to validate the structure and format of incoming URLs.
2. Input length limits: We enforce a maximum URL length to prevent potential buffer overflow attacks.
3. Allowed schemes: We restrict URLs to use only http and https schemes.
4. Secure