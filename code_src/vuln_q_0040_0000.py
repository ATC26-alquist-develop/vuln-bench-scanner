from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import ssl

app = Flask(__name__)

# Rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure secret key generation
app.config['SECRET_KEY'] = os.urandom(24)

# Only allow specific origins
ALLOWED_ORIGINS = [
    'https://trusted-domain.com',
    'https://another-trusted-domain.com'
]

@app.before_request
def check_origin():
    """Validate origin before processing request"""
    origin = request.headers.get('Origin')
    if origin not in ALLOWED_ORIGINS:
        return jsonify({'error': 'Origin not allowed'}), 403

@app.route('/api', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Additional rate limiting
def secure_endpoint():
    """Example secure endpoint"""
    return jsonify({'message': 'Request processed securely'})

if __name__ == '__main__':
    # SSL/TLS configuration
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile='path/to/cert.pem',
        keyfile='path/to/key.pem'
    )
    
    # Bind to localhost only
    app.run(
        host='127.0.0.1',  # Localhost
        port=8443,  # Non-standard port
        ssl_context=context,
        debug=False  # Don't enable debug mode in production
    )