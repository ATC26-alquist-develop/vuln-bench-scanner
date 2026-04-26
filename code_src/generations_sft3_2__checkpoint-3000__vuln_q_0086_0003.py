from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
def setup_logging():
    """Configure secure logging"""
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
    
    # Configure Flask app
    app = Flask(__name__)
    
    # Enable HTTPS
    if os.environ.get('FLASK_ENV') == 'production':
        app.config['SERVER_NAME'] = 'yourdomain.com:443'
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Set secure headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    return app

app = setup_logging()

# Rate limiting to prevent abuse
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Example protected route
@app.route('/protected')
@limiter.limit("10 per minute")
def protected():
    """Example protected route"""
    return "This is a protected route"

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',  # Only listen on localhost
        port=5000,  # Use a non-privileged port
        ssl_context='adhoc' if os.environ.get('FLASK_ENV') == 'production' else None
    )