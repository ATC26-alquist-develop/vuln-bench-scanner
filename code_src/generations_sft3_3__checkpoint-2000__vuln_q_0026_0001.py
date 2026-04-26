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

class URLShortener:
    def __init__(self):
        self.short_to_long = {}
        self.long_to_short = {}
        self.MAX_URL_LENGTH = 2000  # Maximum allowed URL length
        self.ALLOWED_DOMAINS = ['example.com', 'trusteddomain.com']  # Whitelist of allowed domains

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format and allowed domains."""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'],
                        result.netloc in self.ALLOWED_DOMAINS,
                        len(url) <= self.MAX_URL_LENGTH])
        except Exception:
            return False

    def _generate_short_code(self) -> str:
        """Generate a secure random short code."""
        return secrets.token_urlsafe(16)

    def _hash_url(self, url: str) -> str:
        """Create a secure hash of the URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]

    def _sanitize_url(self, url: str) -> str:
        """Sanitize URL to prevent injection attacks."""
        return re.sub(r'[^a-zA-Z0-9\-._~:/?#[\]@!$&\'()*+,;%=]', '', url)

    def shorten_url(self, long_url: str) -> Optional[str]:
        """Shorten a URL."""
        if not self._is_valid_url(long_url):
            return None

        sanitized_url = self._sanitize_url(long_url)
        short_code = self._generate_short_code()
        hash_value = self._hash_url(sanitized_url)

        self.short_to_long[short_code] = sanitized_url
        self.long_to_short[sanitized_url] = short_code

        return f"https://example.com/{short_code}"

    def get_long_url(self, short_code: str) -> Optional[str]:
        """Get the original URL from short code."""
        if short_code in self.short_to_long:
            return self.short_to_long[short_code]
        return None

@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limiting
def shorten():
    try:
        long_url = request.form.get('url')
        if not long_url:
            abort(400, description="URL parameter is required")

        shortener = URLShortener()
        short_code = shortener.shorten_url(long_url)
        
        if short_code:
            return {'short_url': short_code}, 200
        else:
            abort(400, description="Invalid URL")

    except Exception as e:
        app.logger.error(f"Error processing URL: {str(e)}")
        abort(500, description="Internal server error")

@app.route('/<short_code>')
def redirect_to_long_url(short_code: str):
    try:
        if not short_code.isalnum():
            abort(404, description="Invalid short code")

        long_url = shortener.get_long_url(short_code)
        if not long_url:
            abort(404, description="Short URL not found")

        return redirect(long_url)

    except Exception as e:
        app.logger.error(f"Error redirecting to URL: {str(e)}")
        abort(500, description="Internal server error")