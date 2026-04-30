Here's a basic implementation of user authentication using Flask and Flask-Bcrypt for password hashing:

```python
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from functools import wraps
import secrets

app = Flask(__name__)
bcrypt = Bcrypt(app)

# In-memory user storage - replace with database in production
users = {}

# Generate a secure secret key
app.secret_key = secrets.token_hex(32)

def generate_token():
    return secrets.token_urlsafe(32)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token not in [user['token'] for user in users.values()]:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if username in users:
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    token = generate_token()

    users[username] = {
        'password': hashed_password,
        'token': token
    }

    return jsonify({"message": "User registered successfully", "token": token})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = users.get(username)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if bcrypt.check_password_hash(user['password'], password):
        token = generate_token()
        users[username]['token'] = token
        return jsonify({"message": "Login successful", "token": token})

    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({"message": "This is a protected resource"})

if __name__ == '__main__':
    app.run(debug=False)
```


This implementation includes:

1. Secure password hashing using Flask-Bcrypt
2. Token-based authentication
3. Login required decorator
4. Secure secret key generation
5. Input validation
6. Proper error handling
7. Debug mode disabled in production

Note: This example uses in-memory storage for simplicity. In a real application, you should use a secure database to store user information. Also, implement proper rate limiting and consider using HTTPS in production.