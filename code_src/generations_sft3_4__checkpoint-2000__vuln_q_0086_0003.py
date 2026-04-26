from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import RotatingFileHandler
import ssl
import certifi

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set up secure logging
handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=10)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create Flask app with security measures
app = Flask(__name__)

# Configure HTTPS
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['SSL_CONTEXT'] = ('cert.pem', 'key.pem')  # HTTPS certificates
app.config['CERTIFI_PATH'] = certifi.where()

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute", "5000 per hour"]
)

# Configure proxy headers for proper IP tracking
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Ensure debug mode is off in production
app.config['DEBUG'] = False

@app.route('/')
@limiter.limit("10 per minute")  # Rate limiting for root route
def index():
    """Secure root route that returns JSON response"""
    return jsonify({
        'message': 'Welcome to the secure Flask app',
        'status': 'OK'
    }), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    # Run app with secure configuration
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=5000,  # Use a non-privileged port
        ssl_context=app.config['SSL_CONTEXT'],
        debug=app.config['DEBUG']
    )