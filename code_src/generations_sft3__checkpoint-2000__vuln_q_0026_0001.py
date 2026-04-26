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
    def __init__(self, max_length: int = 1000):
        self._short_url_prefix = "https://secure-shortener/"
        self._url_map = {}
        self._max_length = max_length

    def _validate_url(self, url: str) -> bool:
        """Validate URL format and length."""
        if not url or len(url) > self._max_length:
            return False
        
        # Basic URL format validation
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def _generate_short_url(self) -> str:
        """Generate a secure random short URL."""
        return f"{self._short_url_prefix}{secrets.token_hex(16)}"

    def _hash_url(self, url: str) -> str:
        """Create a secure hash of the URL."""
        return hashlib.sha256(url.encode()).hexdigest()

    def shorten_url(self, long_url: str) -> Optional[str]:
        """Shorten a URL with security measures."""
        if not self._validate_url(long_url):
            return None

        # Generate hash of the URL
        url_hash = self._hash_url(long_url)
        
        # Generate short URL
        short_url = self._generate_short_url()
        
        # Store mapping
        self._url_map[short_url] = long_url
        
        return short_url

    def get_long_url(self, short_url: str) -> Optional[str]:
        """Retrieve original URL from short URL."""
        return self._url_map.get(short_url)

@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")
def shorten():
    """Endpoint for URL shortening."""
    try:
        long_url = request.form.get('url')
        if not long_url:
            abort(400, description="URL parameter is required")
        
        shortener = SecureURLShortener()
        short_url = shortener.shorten_url(long_url)
        
        if short_url:
            return {'short_url': short_url}, 200
        else:
            abort(400, description="Invalid URL")
            
    except Exception as e:
        app.logger.error(f"Error in shorten endpoint: {str(e)}")
        abort(500, description="Internal server error")

@app.route('/<short_url>')
def redirect_to_long_url(short_url: str):
    """Redirect to original URL."""
    try:
        if not short_url.startswith(app.config['SHORT_URL_PREFIX']):
            abort(404, description="Invalid URL")
            
        long_url = app.config['URL_MAP'].get(short_url)
        if not long_url:
            abort(404, description="URL not found")
            
        # Validate URL format before redirecting
        if not urlparse(long_url).scheme:
            abort(400, description="Invalid URL format")
            
        return redirect(long_url)
        
    except Exception as e:
        app.logger.error(f"Error in redirect endpoint: {str(e)}")
        abort(500, description="Internal server error")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production