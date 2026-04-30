from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import ssl

app = Flask(__name__)

# Rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure secret key generation
app.config['SECRET_KEY'] = os.urandom(24)

# HTTPS only
if not os.environ.get('HTTPS_ONLY', '0') == '1':
    app.config['SSL_CONTEXT'] = ssl.create_default_context()
    app.config['SSL_CERT'] = os.environ.get('SSL_CERT_PATH')
    app.config['SSL_KEY'] = os.environ.get('SSL_KEY_PATH')

@app.route('/api', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Additional rate limiting for API
def secure_api():
    # Implement your secure logic here
    return jsonify({"message": "Secure API response"})

if __name__ == '__main__':
    # Bind to all interfaces, but only on localhost for development
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(host='127.0.0.1', port=443, ssl_context=app.config['SSL_CONTEXT'])
    else:
        app.run(host='0.0.0.0', port=5000, debug=False)