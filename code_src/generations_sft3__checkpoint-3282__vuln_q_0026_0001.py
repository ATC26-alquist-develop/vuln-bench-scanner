```python
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

# Secure Redis connection for short codes storage
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

    def _store_url(self, long_url: str, short_code: str) -> None:
        """Store URL mapping in Redis."""
        redis_client.setex(
            short_code,
            86400,  # 24 hours
            long_url
        )

    def _get_long_url(self, short_code: str) -> Optional[str]:
        """Retrieve long URL from Redis."""
        return redis_client.get(short_code)

    def shorten_url(self, long_url: str) -> Optional[str]:
        """Shorten a URL."""
        if not self._is_valid_url(long_url):
            logger.warning(f"Invalid URL attempted: {long_url}")
            return None

        # Generate short code
        short_code = self._generate_short_code()
        
        # Store URL mapping
        self._store_url(long_url, short_code)
        
        # Construct shortened URL
        return self.base_url + short_code

    def expand_url(self, short_code: str) -> Optional[str]:
        """Expand a short code to long URL."""
        long_url = self._get_long_url(short_code)
        if long_url is None:
            logger.warning(f"Short code not found: {short_code}")
            return None
            
        return long_url

@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")
def shorten():
    """Endpoint for URL shortening."""
    try:
        long_url = request.form.get('url')
        if not long_url:
            return 'Missing URL parameter', 400
            
        short_code = URLShortener().shorten_url(long_url)
        if not short_code:
            return 'Invalid URL', 400
            
        return {'short_url': short_code}, 200
    except Exception as e:
        logger.error(f"Error in shorten endpoint: {str(e)}")
        return 'Internal server error', 500

@app.route('/expand/<short_code>', methods=['GET'])
@limiter.limit("10 per minute")
def expand(short_code: str):
    """Endpoint for URL expansion."""
    try:
        long_url = URLShortener().expand_url(short_code)
        if not long_url:
            return 'Short code not