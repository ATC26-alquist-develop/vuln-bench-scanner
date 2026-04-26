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
app.config['SSL_CONTEXT'] = ('cert.pem', 'key.pem')  # Load your SSL certificate and key

# Enable HTTPS
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute", "5000 per hour"]
)

# Secure headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Secure error handling
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

# Main route
@app.route('/')
@limiter.limit("10 per minute")  # Rate limit home page
def index():
    return jsonify({"message": "Welcome to secure Flask app"})

if __name__ == '__main__':
    # Start server with secure configuration
    app.run(
        host='127.0.0.1',  # Only listen on localhost
        port=5000,
        ssl_context=app.config['SSL_CONTEXT'],
        debug=False,  # Ensure debug mode is off in production
        use_reloader=False
    )