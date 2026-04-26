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
        'username': 'john_doe',
        'email': 'john@example.com',
        'full_name': 'John Doe'
    }
}

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    # Remove any HTML tags
    text = bleach.clean(text, tags=[], strip=True)
    # Escape HTML special characters
    text = html.escape(text)
    return text

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@app.route('/profile', methods=['GET'])
@login_required
def user_profile():
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

        # Sanitize all user data
        sanitized_user = {
            'username': sanitize_input(user['username']),
            'email': sanitize_input(user['email']),
            'full_name': sanitize_input(user['full_name'])
        }

        return render_template(
            'profile.html',
            user=sanitized_user,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        # Log error securely - don't expose details to user
        app.logger.error(f"Error displaying profile: {str(e)}")
        abort(500)  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode off in production