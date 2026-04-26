from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import RotatingFileHandler

# Configure secure logging
def setup_logging():
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
setup_logging()

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Ensure HTTPS
if not os.environ.get('FLASK_RUN_SSL'):
    raise EnvironmentError("HTTPS not enabled. Set FLASK_RUN_SSL=1 to enable HTTPS")

# Configure proxy headers for proper IP detection
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/')
@limiter.limit("100 per minute")  # Rate limiting for root route
def index():
    return "Welcome to Secure Flask App"

if __name__ == '__main__':
    # Run app with HTTPS
    app.run(
        ssl_context='adhoc',  # Use adhoc SSL for development
        host='127.0.0.1',  # Bind to localhost only
        port=5000
    )