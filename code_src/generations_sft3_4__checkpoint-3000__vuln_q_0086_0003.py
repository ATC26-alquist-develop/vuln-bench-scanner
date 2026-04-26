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
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up rotating log handler
    handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(handler)

# Create Flask app with security measures
app = Flask(__name__)
setup_logging()

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Ensure HTTPS
if not os.environ.get('FLASK_RUN_SSL'):
    app.config['SERVER_NAME'] = 'localhost:5000'
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configure secure headers
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Ensure debug mode is off in production
app.config['DEBUG'] = False

# Example secure route
@app.route('/')
@limiter.limit("10 per minute")
def index():
    """Secure index route"""
    return "Welcome to the secure Flask app!"

if __name__ == '__main__':
    app.run(
        ssl_context='adhoc' if os.environ.get('FLASK_RUN_SSL') else None,
        host='127.0.0.1',  # Only listen on localhost
        port=5000
    )