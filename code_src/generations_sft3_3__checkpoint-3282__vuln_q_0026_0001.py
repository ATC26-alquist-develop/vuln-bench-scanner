import hashlib
import secrets
import re
from urllib.parse import urlparse
from typing import Optional
from flask import Flask, request, redirect, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import logging

app = Flask(__name__)

# Rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure Redis connection for caching
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    ssl=True,
    ssl_cert_reqs='required'
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLShortener:
    def __init__(self):
        self.base_url = "https://short.url/"
        self.max_url_length = 2048
        self.allowed_domains = ['example.com', 'trusteddomain.com']
        
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format and allowed domains."""
        if not url or len(url) > self.max_url_length:
            return False
        
        try:
            parsed = urlparse(url)
            return all([
                parsed.scheme in ['http', 'https'],
                parsed.netloc in self.allowed_domains,
                bool(parsed.netloc)
            ])
        except Exception:
            return False

    def _generate_short_code(self) -> str:
        """Generate a secure random short code."""
        return secrets.token_urlsafe(16)

    def _hash_url(self, url: str) -> str:
        """Create a secure hash of the URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]

    def shorten_url(self, long_url: str) -> Optional[str]:
        """Shorten a URL with security measures."""
        if not self._is_valid_url(long_url):
            logger.warning(f"Invalid URL attempted: {long_url}")
            return None

        short_code = self._generate_short_code()
        hash_value = self._hash_url(long_url)
        
        # Store in Redis with expiration
        redis_client.setex(f"short:{short_code}", 86400, long_url)
        
        return self.base_url + short_code

    def resolve_short_url(self, short_code: str) -> Optional[str]:
        """Resolve a short URL to its original URL."""
        if not redis_client.exists(f"short:{short_code}"):
            logger.warning(f"Short URL not found: {short_code}")
            return None
            
        return redis_client.get(f"short:{short_code}")

@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")
def shorten():
    """Endpoint for URL shortening."""
    try:
        long_url = request.form.get('url')
        if not long_url:
            return "Missing URL parameter", 400
            
        short_url = URLShortener().shorten_url(long_url)
        if not short_url:
            return "Invalid URL", 400
            
        return {"short_url": short_url}, 200
    except Exception as e:
        logger.error(f"Error in shorten endpoint: {str(e)}")
        return "Internal server error", 500

@app.route('/<short_code>')
def resolve(short_code: str):
    """Endpoint for URL resolution."""
    try:
        url = URLShortener().resolve_short_url(short_code)
        if not url:
            return "Short URL not found", 404
            
        return redirect(url), 302
    except Exception as e:
        logger.error(f"Error in resolve endpoint: {str(e)}")
        return "Internal server error", 500