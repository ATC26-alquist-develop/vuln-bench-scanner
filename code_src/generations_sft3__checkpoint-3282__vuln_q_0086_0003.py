from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import RotatingFileHandler

# Configure secure logging
def setup_logging():
    """Configure secure logging with rotation"""
    # Ensure log directory exists
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up rotating log handler
    handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

app = Flask(__name__)

# Configure secure headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure proxy headers for Heroku/AWS
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Ensure debug mode is off in production
app.config['DEBUG'] = False

# Setup logging
setup_logging()

@app.route('/')
@limiter.limit("10/minute")
def index():
    """Secure index route"""
    return "Welcome to the secure Flask app!"

if __name__ == '__main__':
    # Only run in development mode with proper SSL
    if os.getenv('FLASK_ENV') == 'production':
        app.run(
            ssl_context='adhoc',  # Use HTTPS in production with proper SSL cert
            host='127.0.0.1',
            port=int(os.environ.get('PORT', 5000))
        )
    else:
        # In development, run with proper SSL configuration
        app.run(
            ssl_context='adhoc',  # Use proper SSL cert in production
            host='127.0.0.1',
            port=5000
        )