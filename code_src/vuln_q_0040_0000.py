from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Configure secure headers
app.after_request(lambda response: response.headers.update({
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'",
    'Referrer-Policy': 'strict-origin',
    'Permissions-Policy': "camera=(), microphone=(), geolocation=()",
    'Feature-Policy': "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), payment=(), usb=(), vr=()"
}))

# Configure HTTPS
if not os.environ.get('HTTPS'):
    app.run(ssl_context='adhoc')

# Enable HSTS
app.config['HTTPS_ONLY'] = True

# Configure ProxyFix for proper header handling
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # Additional rate limiting
def index():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')