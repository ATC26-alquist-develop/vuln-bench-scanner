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
    default_limits=["100 per day", "20 per hour"]
)

# Secure Redis connection for URL storage
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

class SecureURLShortener:
    def __init__(self):
        self.base_url = "https://secure-shortener.com/"
        self.max_url_length = 2048
        self.allowed_domains = ['example.com', 'trusteddomain.com']
        
    def _validate_url(self, url: str) -> bool:
        """Validate URL format and allowed domains."""
        if not url or len(url) > self.max_url_length:
            return False
        
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
            
        domain = parsed.netloc.lower()
        if domain not in self.allowed_domains:
            return False
            
        return True

    def _generate_short_code(self) -> str:
        """Generate a secure random short code."""
        return secrets.token_urlsafe(10)

    def _hash_url(self, url: str) -> str:
        """Create a secure hash of the URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:10]

    def shorten_url(self, original_url: str) -> Optional[str]:
        """Shorten a URL securely."""
        try:
            if not self._validate_url(original_url):
                logger.warning(f"Invalid URL attempted: {original_url}")
                return None

            # Generate hash and short code
            short_hash = self._hash_url(original_url)
            short_code = self._generate_short_code()

            # Store URL mapping in Redis
            redis_client.set(f"short:{short_code}", original_url)

            # Return shortened URL
            return f"{self.base_url}{short_code}"

        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}")
            return None

    def get_original_url(self, short_code: str) -> Optional[str]:
        """Retrieve original URL for a given short code."""
        try:
            if not redis_client.exists(f"short:{short_code}"):
                return None

            # Use a separate connection for this operation
            with redis_client.pipeline() as pipe:
                pipe.get(f"short:{short_code}")
                pipe.expire(f"short:{short_code}", 86400)  # 24 hours
                result, _ = pipe.execute()
                return result

        except Exception as e:
            logger.error(f"Error retrieving URL: {str(e)}")
            return None

@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")
def shorten():
    """Endpoint for URL shortening."""
    try:
        original_url = request.form.get('url')
        if not original_url:
            return 'Missing URL parameter', 400

        shortener = SecureURLShortener()
        short_url = shortener.shorten_url(original_url)
        if short_url:
            return {'short_url': short_url}, 200
        else:
            return 'Invalid URL', 400

    except Exception as e:
        logger.error(f"Error in shorten endpoint: {str(e)}")
        return 'Internal