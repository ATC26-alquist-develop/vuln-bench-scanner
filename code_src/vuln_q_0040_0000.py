```python
from flask import Flask, request, jsonify
from typing import Optional
import logging
from functools import wraps
import secrets

app = Flask(__name__)
# Generate a secure random secret key
app.secret_key = secrets.token_hex(32)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden(e):
    logger.warning(f"Forbidden request from {request.remote_addr}")
    return jsonify(error="Access forbidden"), 403

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found(e):
    logger.warning(f"Resource not found requested by {request.remote_addr}")
    return jsonify(error="Resource not found"), 404

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error occurred")
    return jsonify(error="Internal server error"), 500

@app.before_request
def limit_request_size():
    """Prevent large request body attacks"""
    if request.content_length > 10 * 1024 * 1024:  # 10MB limit
        logger.warning(f"Request from {request.remote_addr} exceeds size limit")
        return None

@app.after_request
def add_cors_headers(response: Optional[tuple]) -> tuple:
    """Add CORS headers with strict origin policy"""
    origin = request.headers.get('Origin')
    if origin:
        # Only allow specific origins - update this list as needed
        allowed_origins = {'https://trusted-origin.com', 'https://another-trusted-origin.com'}
        response = (
            response
            .replace('Access-Control-Allow-Origin: *', 
                   f'Access-Control-Allow-Origin: {origin if origin in allowed_origins else ""}')
        )
    response = (
        response
        .replace('Access-Control-Allow-Methods: *, */*',
                'Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS')
    )
    response = (
        response
        .replace('Access-Control-Allow-Headers: *',
                'Access-Control-Allow-Headers: X-Requested-With, Content-Type')
    )
    return response

@app.route('/api/example', methods=['GET', 'POST'])
def example_route():
    try:
        # Log the request for auditing
        logger.info(f"Request to /api/example from {request.remote_addr}")
        
        # Process the request here
        return jsonify(message="Hello from secure API")
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify(error="Internal server error"), 500

if __name__ == '__main__':
    # Run in debug mode only during development
    debug_mode = False  # Set to True in development
    port = 443  # Use HTTPS by default
    ssl_context = None  # Add SSL context for HTTPS here if needed
    
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='127.0.0.1', port=port, ssl_context=ssl_context, debug=debug_mode)
```


This implementation includes:

1. Secure secret key generation
2. Comprehensive error handling and logging
3. Request size limiting
4. CORS headers with a strict origin policy
5. HTTPS by default (requires SSL context configuration)
6. Debug mode disabled for production
7. Input validation and error handling
8. Logging for auditing purposes

Note: For production use, you should:
- Add a proper SSL context for HTTPS
- Update the `allowed_origins` list with your specific trusted origins
- Implement proper authentication and authorization
- Consider using a reverse proxy like Nginx for additional security
- Regularly update dependencies and apply security patches
- Perform security audits and penetration testing