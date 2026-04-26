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

# Secure secret key generation
SECRET_KEY = secrets.token_bytes(32)

def is_valid_url(url: str) -> bool:
    """Validate URL format and scheme."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False

def generate_short_code(length: int = 7) -> str:
    """Generate cryptographically secure random short code."""
    return secrets.token_hex(length)

def hash_url(url: str) -> str:
    """Create secure hash of URL."""
    return hashlib.sha256(url.encode()).hexdigest()[:10]

@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limiting for this endpoint
def shorten_url():
    try:
        url = request.form.get('url')
        if not url or not is_valid_url(url):
            abort(400, description="Invalid URL format")
        
        # Generate secure hash of the URL
        hashed_url = hash_url(url)
        
        # Generate secure short code
        short_code = generate_short_code()
        
        # Store mapping (in production, use a secure database)
        # This is a simplified example - use proper database in production
        url_map = {
            hashed_url: short_code
        }
        
        return {
            'short_url': f'https://yourdomain.com/{short_code}'
        }, 200

    except Exception as e:
        app.logger.error(f"Error processing URL: {str(e)}")
        abort(500, description="Internal server error")

@app.route('/<short_code>')
def redirect_to_url(short_code: str):
    try:
        # Validate short code format
        if not re.match(r'^[a-f0-9]{8,10}$', short_code):
            abort(404, description="Invalid short URL")
            
        # Retrieve original URL
        hashed_url = hash_url(f'https://yourdomain.com/{short_code}')
        if hashed_url not in url_map:
            abort(404, description="URL not found")
            
        return redirect(url_map[hashed_url])
        
    except Exception as e:
        app.logger.error(f"Error redirecting URL: {str(e)}")
        abort(500, description="Internal server error")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper certificates