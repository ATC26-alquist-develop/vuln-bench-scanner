```python
import secrets
import hashlib
from urllib.parse import urlparse, urlunparse
from typing import Optional
import re
from flask import Flask, request, redirect, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "20 per hour"]
)

class SecureURLShortener:
    def __init__(self, max_length: int = 100):
        self._short_url_prefix = "https://secure-shortener/"
        self._url_map = {}
        self._max_length = max_length

    def _validate_url(self, url: str) -> bool:
        """Validate URL format and scheme."""
        if not url or len(url) > self._max_length:
            return False
        
        # Validate URL format
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def _generate_short_url(self) -> str:
        """Generate a secure random short URL."""
        return f"{self._short_url_prefix}{secrets.token_hex(8)}"

    def _hash_url(self, url: str) -> str:
        """Create a secure hash of the URL."""
        return hashlib.sha256(url.encode()).hexdigest()

    def shorten_url(self, original_url: str) -> Optional[str]:
        """Shorten a URL securely."""
        if not self._validate_url(original_url):
            return None

        # Generate hash of the URL
        url_hash = self._hash_url(original_url)
        
        # Check if URL already exists
        if url_hash in self._url_map:
            return self._url_map[url_hash]

        # Generate new short URL
        short_url = self._generate_short_url()
        
        # Store mapping
        self._url_map[url_hash] = short_url
        
        return short_url

    def get_original_url(self, short_url: str) -> Optional[str]:
        """Retrieve original URL from short URL."""
        if not short_url.startswith(self._short_url_prefix):
            return None

        # Remove prefix
        url_hash = short_url[len(self._short_url_prefix):]
        
        # Check if URL exists
        if url_hash in self._url_map:
            return self._url_map[url_hash]
        
        return None

@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limiting
def shorten():
    try:
        original_url = request.form.get('url')
        if not original_url:
            abort(400, description="Missing URL parameter")

        shortener = SecureURLShortener()
        short_url = shortener.shorten_url(original_url)
        
        if short_url:
            return {'short_url': short_url}, 200
        else:
            abort(400, description="Invalid URL")

    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        abort(500, description="Internal server error")

@app.route('/<short_url>')
def redirect_to_original(short_url: str):
    try:
        shortener = SecureURLShortener()
        original_url = shortener.get_original_url(short_url)
        
        if not original_url:
            abort(404, description="Short URL not found")
        
        # Validate URL scheme
        parsed_url = urlparse(original_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            abort(400, description="Invalid URL")

        return redirect(original_url, code=302)

    except Exception as e:
        app.logger.error(f"Error redirecting to URL: