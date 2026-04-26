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

def sanitize_input(input_string: str) -> str:
    """Sanitize user input to prevent XSS"""
    # Remove any HTML tags
    text = bleach.clean(input_string, tags=[], strip=True)
    # Escape HTML special characters
    return html.escape(text)

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@app.route('/profile', methods=['GET'])
@login_required
def profile_page() -> str:
    """Display user profile page"""
    try:
        # Get user ID from session
        user_id = current_user.get_id()
        if not user_id:
            abort(401)  # Unauthorized
        
        # Get user data
        user = USERS.get(int(user_id))
        if not user:
            abort(404)  # Not Found
            
        # Prepare sanitized data
        profile_data: Dict[str, Any] = {
            'id': user['id'],
            'username': user['username'],
            'full_name': sanitize_input(user['full_name']),
            'email': sanitize_input(user['email'])
        }
        
        return render_template(
            'profile.html',
            profile_data=profile_data,
            user=current_user
        )
        
    except Exception as e:
        # Log error securely without exposing details
        app.logger.error(f"Error in profile page: {str(e)}")
        abort(500)  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode off in production