import logging
from flask import Flask, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import BadRequest
import os
from pathlib import Path

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure file path for logs
LOG_FILE = Path("/var/log/app/app.log")

@app.route('/logs', methods=['GET'])
@limiter.limit("10 per minute")  # Rate limit to 10 calls per minute
def get_logs():
    """
    Securely retrieve system logs.
    Returns a JSON response with the last 100 lines of the log file.
    """
    try:
        # Ensure the log file exists and is readable
        if not LOG_FILE.is_file() or not os.access(LOG_FILE, os.R_OK):
            logger.error("Log file not accessible")
            abort(404, description="Log file not found or not readable")

        # Read last 100 lines of the log file
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()[-100:]
        
        # Sanitize log lines
        sanitized_lines = [line.strip() for line in lines if line.strip()]
        
        return jsonify({"logs": sanitized_lines})

    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}")
        abort(500, description="Internal server error")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)