from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a secure random secret key

# Mock database (replace with a real database in production)
users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Hash the password before storing
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    stored_password = users.get(username)
    if stored_password and check_password_hash(stored_password, password):
        session['user'] = username
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False in production