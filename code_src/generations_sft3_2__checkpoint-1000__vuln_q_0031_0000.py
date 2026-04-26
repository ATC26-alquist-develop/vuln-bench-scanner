import os
from flask import Flask, abort, send_file
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler
import hashlib
import time

app = Flask(__name__)

# Configure logging
log_dir = '/var/log/myapp'  # Adjust this path as needed
if not os.path.exists(log_dir):
    os.makedirs(log_dir, mode=0o750)  # Secure permissions

log_file = os.path.join(log_dir, 'system.log')
handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/logs')
def get_logs():
    """
    Securely retrieve system logs.
    Returns:
        str: Log file content
    """
    try:
        # Generate a unique filename based on timestamp
        timestamp = int(time.time())
        filename = f"system_log_{timestamp}.log"
        log_path = os.path.join(log_dir, secure_filename(filename))
        
        # Ensure the file exists and has proper permissions
        if not os.path.exists(log_path):
            app.logger.error("Log file not found")
            abort(404)
        
        # Verify file permissions
        if not os.access(log_path, os.R_OK):
            app.logger.error("Insufficient permissions to read log file")
            abort(403)
        
        # Read and return the log file content
        with open(log_path, 'r') as f:
            log_content = f.read()
        
        return log_content, 200, {'Content-Type': 'text/plain'}
    
    except Exception as e:
        app.logger.error(f"Error retrieving logs: {str(e)}")
        abort(500)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, ssl_context='adhoc')  # Use HTTPS in production