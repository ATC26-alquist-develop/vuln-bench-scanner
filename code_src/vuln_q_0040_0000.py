```python
from flask import Flask, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure allowed origins
ALLOWED_ORIGINS = ['https://trusted-origin.com']  # Add your trusted origins here

@app.before_request
def check_origin():
    """Validate origin before processing request"""
    origin = request.headers.get('Origin', '')
    if origin and origin not in ALLOWED_ORIGINS:
        abort(403)  # Forbidden

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # Additional rate limiting
def secure_endpoint():
    """Handle requests securely"""
    return "Request processed securely"

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',  # Bind to localhost only
        port=5000,  # Use non-standard port
        ssl_context='adhoc'  # Enable HTTPS
    )
```