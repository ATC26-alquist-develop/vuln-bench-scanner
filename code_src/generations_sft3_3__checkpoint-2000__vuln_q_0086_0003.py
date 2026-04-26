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

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute", "5000 per hour"]
)

# Configure proxy headers for Heroku/AWS
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/api', methods=['GET'])
@limiter.limit("10 per minute")  # Rate limiting for API endpoints
def api():
    """Secure API endpoint example"""
    try:
        # Validate and sanitize input
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if not ip:
            return jsonify({"error": "Invalid IP"}), 400
        
        # Process request
        response = {
            "message": "Hello from secure Flask app",
            "ip": ip
        }
        logger.info(f"Request from {ip}")
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error in API endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Ensure SSL context is loaded
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        raise RuntimeError("SSL certificate and key not found")
    
    # Run app with HTTPS
    app.run(ssl_context='SSL_CONTEXT', host='0.0.0.0', port=5000)