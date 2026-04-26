import secrets
import hashlib
from urllib.parse import urlparse
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
    default_limits=["100 per day", "10 per hour"]
)

# Whitelist of allowed domains
ALLOWED_DOMAINS = {'example.com', 'trusteddomain.com'}

def is_valid_url(url: str) -> bool:
    """Validate URL format and allowed domains."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], 
                   result.netloc in ALLOWED_DOMAINS,
                   re.match(r'^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}', result.netloc)])
    except Exception:
        return False

def generate_short_code(length: int = 6) -> str:
    """Generate cryptographically secure random short code."""
    return secrets.token_hex(length)

def hash_url(url: str) -> str:
    """Create a secure hash of the URL."""
    return hashlib.sha256(url.encode()).hexdigest()[:6]

@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")
def shorten_url():
    try:
        # Get URL from request
        url = request.form.get('url')
        
        # Validate URL
        if not url or not is_valid_url(url):
            abort(400, description="Invalid or disallowed URL")
            
        # Generate short code
        short_code = generate_short_code()
        short_url = f"https://example.com/short/{short_code}"
        
        # Store URL mapping (in production, use a secure database)
        # This is a simplified example
        url_map = {
            url: short_url
        }
        
        return redirect(short_url)
        
    except Exception as e:
        # Log error securely (implement proper logging)
        abort(500, description="Internal server error")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate