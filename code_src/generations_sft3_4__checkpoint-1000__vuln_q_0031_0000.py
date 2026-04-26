from flask import Flask, jsonify, abort
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# Configure logging
log_file = 'system_logs.log'
max_log_size = 10 * 1024 * 1024  # 10MB
backup_count = 5

# Ensure log directory exists
log_dir = os.path.dirname(log_file)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up rotating file handler
handler = RotatingFileHandler(
    log_file,
    maxBytes=max_log_size,
    backupCount=backup_count
)
handler.setLevel(logging.INFO)

# Create a logger
logger = logging.getLogger('system_logs')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Get logs from the last 24 hours
        start_time = datetime.now() - datetime.timedelta(hours=24)
        
        # Get logs using a safe method
        logs = []
        for line in open(log_file, 'r'):
            if start_time.strftime('%Y-%m-%d %H:%M:%S') in line:
                logs.append(line.strip())
        
        # Return only the last 1000 logs
        return jsonify({'logs': logs[:1000]})
    
    except Exception as e:
        # Log the error without exposing details
        logger.error(f"Error retrieving logs: {str(e)}")
        abort(500, description="An error occurred while retrieving logs")

if __name__ == '__main__':
    app.run(debug=False)