from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/system-logs', methods=['GET'])
def get_system_logs():
    # Assuming your system logs are stored in a file called 'system.log'
    log_file_path = 'system.log'
    
    if not os.path.exists(log_file_path):
        return jsonify({"error": "Log file not found"}), 404
    
    with open(log_file_path, 'r') as log_file:
        logs = log_file.readlines()
    
    # Optionally, you can process the logs to make them more readable
    processed_logs = [log.strip() for log in logs]
    
    return jsonify({"logs": processed_logs})

if __name__ == '__main__':
    app.run(debug=True)