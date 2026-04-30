from typing import Dict, Optional
from argon2 import PasswordHasher
from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email
from flask import Flask, request, jsonify
import re
import logging
from functools import wraps

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Secure password hasher
ph = PasswordHasher()

class ProfileForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            lambda v: len(re.findall(r'[^\w\s]', v)) < 3  # Limit special characters
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            lambda v: len(v) < 100  # Limit email length
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=128),
            lambda v: ph.verify_hash(v)  # Verify password strength
        ]
    )

def validate_input(data: Dict) -> bool:
    """Validate input data with strict rules."""
    try:
        # Validate required fields
        if not all(key in data for key in ['username', 'email', 'password']):
            return False
            
        # Validate username
        if not isinstance(data['username'], str) or not data['username']:
            return False
            
        # Validate email
        if not isinstance(data['email'], str) or not data['email']:
            return False
        if '@' not in data['email'] or '.' not in data['email']:
            return False
            
        # Validate password
        if not isinstance(data['password'], str) or not data['password']:
            return False
            
        # Additional validation for username (alphanumeric + underscore)
        if not re.match(r'^[a-zA-Z0-9_]+$', data['username']):
            return False
            
        # Additional validation for email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            return False
            
        return True
    except Exception as e:
        logger.error(f"Input validation error: {str(e)}")
        return False

def rate_limit(max_calls: int = 5, time_window: int = 60):
    """Rate limiting decorator."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            from functools import lru_cache
            cache = lru_cache(maxsize=max_calls)
            try:
                calls = cache(*args, **kwargs)
                if calls > max_calls:
                    return jsonify({"error": "Rate limit exceeded"}), 429
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Rate limiting error: {str(e)}")
                return jsonify({"error": "Internal server error"}), 500
        return wrapped
    return decorator

@app.route('/update_profile', methods=['POST'])
@rate_limit(max_calls=5, time_window=60)
def update_profile():
    try:
        # Get form data
        form_data = request.json
        if not form_data:
            return jsonify({"error": "No data provided"}), 400

        # Validate input
        if not validate_input(form_data):
            return jsonify({"error": "Invalid input"}), 400

        # Create form instance and validate
        profile_form = ProfileForm(data=form_data)
        if not profile_form.validate():
            return jsonify({"error": "Validation failed"}), 400

        # Process data