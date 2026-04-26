from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import RotatingFileHandler
import ssl

app = Flask(__name__)

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Configure HTTPS
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute", "5000 per hour"]
)

# Configure proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/api')
@limiter.limit("10 per minute")
def api():
    """Secure API endpoint"""
    try:
        # Validate and sanitize input
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid input"}), 400

        # Process data (example)
        result = {"status": "success", "data": data}
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Only run on localhost
    app.run(
        host='127.0.0.1',
        port=5000,
        ssl_context=ssl_context,
        debug=False
    )