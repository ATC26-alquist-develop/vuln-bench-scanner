from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app = Flask(__name__)
app.logger.addHandler(handler)

# Configure security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
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

# Secure secret key generation
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
@limiter.limit("10/minute")
def index():
    """Secure index route"""
    return "Welcome to the secure Flask app!"

if __name__ == '__main__':
    # Only run on localhost for production
    app.run(host='127.0.0.1', port=5000, ssl_context='adhoc')