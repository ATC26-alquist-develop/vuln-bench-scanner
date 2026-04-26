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
def profile_page() -> str:
    """Display user profile page"""
    try:
        # Get user ID from session
        user_id = current_user.get_id()
        if not user_id:
            abort(401)  # Unauthorized
        
        user = USERS.get(int(user_id))
        if not user:
            abort(404)  # Not Found
            
        # Get user profile data
        profile_data: Dict[str, Any] = {
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name']
        }
        
        # Sanitize all profile data
        for key in profile_data:
            profile_data[key] = sanitize_input(str(profile_data[key]))
            
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