from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import secrets

app = Flask(__name__)

# Secure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Generate a secure secret key
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Secure configuration
app.config['DEBUG'] = False  # Never run in debug mode in production
app.config['ALLOWED_HOSTS'] = ['localhost', '127.0.0.1']  # Only allow localhost and loopback

@app.route('/api', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Additional rate limiting for API
def api():
    return jsonify({"message": "Secure API endpoint"})

if __name__ == '__main__':
    # Only run on localhost
    if os.getenv('FLASK_ENV') == 'development':
        app.run(host='127.0.0.1', port=5000)
    else:
        print("This is a production environment. Please use a proper WSGI server.")