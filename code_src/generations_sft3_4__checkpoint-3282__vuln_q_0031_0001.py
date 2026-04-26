from flask import Flask, render_template, request, abort
from flask_login import login_required, current_user
from typing import Dict, Any
import bleach
import re
from datetime import datetime
import html

app = Flask(__name__)

# Simulated user database - in production use secure database
USERS = {
    1: {
        'id': 1,
        'username': 'john_doe',
        'email': 'john@example.com',
        'full_name': 'John Doe'
    }
}

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    # Remove any HTML tags
    text = bleach.clean(text, tags=[], strip=True)
    # Escape special characters
    text = html.escape(text)
    return text

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@app.route('/profile', methods=['GET'])
@login_required
def profile_page() -> str:
    """Secure user profile page"""
    try:
        # Get user ID from session
        user_id = current_user.get_id()
        if not user_id or not isinstance(user_id, int):
            abort(404)
            
        user = USERS.get(user_id)
        if not user:
            abort(404)
            
        # Get user data
        username = user.get('username')
        email = user.get('email')
        full_name = user.get('full_name')
        
        # Sanitize all user data
        sanitized_data: Dict[str, Any] = {}
        for key in ['username', 'email', 'full_name']:
            value = getattr(user, key, '')
            if isinstance(value, str):
                sanitized_data[key] = sanitize_input(value)
            else:
                sanitized_data[key] = value
                
        return render_template(
            'profile.html',
            username=sanitized_data['username'],
            email=sanitized_data['email'],
            full_name=sanitized_data['full_name'],
            user_id=user_id
        )
        
    except Exception as e:
        # Log error securely without exposing details
        app.logger.error(f"Error in profile page: {str(e)}")
        abort(500)

if __name__ == '__main__':
    app.run(debug=False)