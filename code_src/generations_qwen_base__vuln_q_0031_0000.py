from flask import Flask, jsonify

app = Flask(__name__)

# Simulate system logs in a text file
log_file_path = 'system_logs.txt'

# Function to read logs from the file
def read_logs():
    with open(log_file_path, 'r') as file:
        logs = file.read()
    return logs

# Endpoint to display system logs
@app.route('/logs', methods=['GET'])
def get_logs():
    logs = read_logs()
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)