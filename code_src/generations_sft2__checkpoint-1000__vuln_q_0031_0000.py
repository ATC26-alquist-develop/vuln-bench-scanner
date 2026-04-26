from flask import Flask, jsonify, abort
import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure logging
log_file = '/var/log/myapp/app.log'
if not os.path.exists(log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Set up secure logging
handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # Implement authentication here
    # For example, check for a valid API key in headers
    api_key = request.headers.get('X-API-Key')
    if not api_key or not is_valid_api_key(api_key):
        abort(401)  # Unauthorized

    # Implement rate limiting here
    # For example, check request count in the last minute
    if is_rate_limit_exceeded():
        abort(429)  # Too Many Requests

    try:
        # Read log file securely
        with open(log_file, 'r') as f:
            logs = f.readlines()

        # Process logs (limit output size and sanitize)
        processed_logs = []
        for log in logs:
            # Remove any potentially dangerous characters
            safe_log = ''.join(char for char in log if char.isprintable())
            if len(safe_log) <= 1000:  # Limit log size
                processed_logs.append(safe_log)

        return jsonify(processed_logs)

    except IOError as e:
        logger.error(f"Error reading log file: {str(e)}")
        abort(500)  # Internal Server Error

def is_valid_api_key(api_key):
    # Implement your API key validation logic here
    # This is a placeholder and should be replaced with actual validation
    return api_key == "your_secure_api_key"

def is_rate_limit_exceeded():
    # Implement rate limiting logic here
    # This is a placeholder and should be replaced with actual rate limiting
    return False

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate