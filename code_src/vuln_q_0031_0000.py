from flask import Flask, jsonify, abort
import os
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure logging
log_file = '/var/log/myapp/app.log'
log_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Secure configuration
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a secure random key
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Limit request size to 1MB

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # Implement rate limiting
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["100 per day", "10 per hour"]
    )
    
    try:
        # Implement rate limiting
        limiter.limit("10 per minute")
        
        # Get logs from secure location
        log_path = '/var/log/myapp/app.log'
        
        # Ensure log file exists and is readable
        if not os.path.exists(log_path) or not os.access(log_path, os.R_OK):
            logger.error("Log file not accessible")
            abort(403)  # Forbidden
        
        # Read logs securely
        with open(log_path, 'r') as log_file:
            logs = log_file.readlines()
        
        # Filter logs (example: show only last 100 entries)
        recent_logs = logs[-100:]
        
        # Sanitize log output
        sanitized_logs = []
        for log in recent_logs:
            # Remove any potentially harmful content
            sanitized_log = log.strip().replace('<', '&lt;').replace('>', '&gt;')
            sanitized_logs.append(sanitized_log)
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'logs': sanitized_logs
        })
    
    except Exception as e:
        logger.error(f"Error accessing logs: {str(e)}")
        abort(500)  # Internal Server Error

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS