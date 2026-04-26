from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.csrf import CSRFProtect
import secrets
import re
from typing import Dict, Any
import bleach

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

class UserProfileForm(FlaskForm):
    """Form for validating user profile data"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=2, max=50)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    bio = StringField(
        'Bio',
        validators=[
            Length(max=500)
        ]
    )
    submit = SubmitField('Save')

def sanitize_input(data: str) -> str:
    """Sanitize user input to prevent XSS"""
    return bleach.clean(data, tags=[], strip=True)

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    """Handle user profile page"""
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    form = UserProfileForm()
    
    if form.validate_on_submit():
        # Sanitize all form fields
        name = sanitize_input(form.name.data)
        email = sanitize_input(form.email.data)
        bio = sanitize_input(form.bio.data)
        
        # Update user profile (implement database update here)
        # Example: update_user_profile(user_id, name, email, bio)
        
        return redirect('/profile')
    
    # Retrieve user profile data
    user_profile = get_user_profile(user_id)
    
    # Sanitize retrieved data
    sanitized_profile = {
        'name': sanitize_input(user_profile.get('name', '')),
        'email': sanitize_input(user_profile.get('email', '')),
        'bio': sanitize_input(user_profile.get('bio', ''))
    }
    
    return render_template('profile.html', 
                           form=form,
                           user_profile=sanitized_profile)

def get_user_profile(user_id: int) -> Dict[str, Any]:
    """Retrieve user profile data from database"""
    # Implement secure database query here
    # Example: return db.get_user_profile(user_id)
    return {'name': 'John Doe', 'email': 'john@example.com', 'bio': 'Hello, I\'m John.'}