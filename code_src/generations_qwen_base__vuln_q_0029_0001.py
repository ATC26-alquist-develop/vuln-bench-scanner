from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# In-memory storage for session data
sessions = {}

@app.route('/run_command', methods=['POST'])
def run_command():
    session_id = request.form.get('session_id')
    command = request.form.get('command')

    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 400

    try:
        # Execute the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        error = result.stderr.decode('utf-8')

        # Store the output and error in the session
        sessions[session_id]['output'] = output
        sessions[session_id]['error'] = error

        return jsonify({"output": output, "error": error})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)