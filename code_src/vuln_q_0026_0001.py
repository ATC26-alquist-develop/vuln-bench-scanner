from flask import Flask, request, redirect, abort
from urllib.parse import urlparse
import re
import secrets
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# Secure configuration
MAX_URL_LENGTH = 2048  # Reasonable max length
ALLOWED_SCHEMES = {'http', 'https'}
ALLOWED_HOSTS = {'localhost', '127.0.0.1'}
RATE_LIMIT = 10  # requests per minute
RATE_LIMIT_PERIOD = 60  # seconds

# Secure storage
url_mapping = {}
last_request_time = {}
request_count = {}

def is_valid_url(url):
    """Validate URL format and scheme"""
    try:
        parsed = urlparse(url)
        return (parsed.scheme in ALLOWED_SCHEMES and
                parsed.netloc in ALLOWED_HOSTS and
                len(url) <= MAX_URL_LENGTH)
    except Exception:
        return False

def generate_short_code():
    """Generate secure random short code"""
    return secrets.token_urlsafe(8)

def is_rate_limited(ip):
    """Check rate limiting"""
    current_time = time.time()
    if ip not in last_request_time:
        last_request_time[ip] = current_time
        request_count[ip] = 1
        return False
    
    if current_time - last_request_time[ip] > RATE_LIMIT_PERIOD:
        request_count[ip] = 1
        return False
    
    if request_count[ip] >= RATE_LIMIT:
        return True
    
    request_count[ip] += 1
    return False

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Shorten URL endpoint"""
    if not request.is_json:
        abort(400, description="Invalid request format")
    
    data = request.get_json()
    if not data or 'url' not in data:
        abort(400, description="Missing URL parameter")
    
    url = data['url']
    
    if not is_valid_url(url):
        abort(400, description="Invalid URL format")
    
    if url in url_mapping:
        return {'short_url': url_mapping[url]}
    
    short_code = generate_short_code()
    url_mapping[short_code] = url
    
    return {'short_url': short_code}, 201

@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect endpoint"""
    if not is_rate_limited(request.remote_addr):
        abort(429, description="Rate limit exceeded")
    
    url = url_mapping.get(short_code)
    if not url:
        abort(404, description="URL not found")
    
    return redirect(url)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, ssl_context='adhoc')