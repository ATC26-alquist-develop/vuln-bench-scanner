from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.csrf import CSRFProtect
import secrets
import re
from typing import Dict, Any

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

class ProfileForm(FlaskForm):
    """Secure form for updating profile information"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=50, message='Username must be 3-50 characters')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email format')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            Length(min=8, max=128, message='Password must be 8-128 characters')
        ]
    )
    submit = SubmitField('Update Profile')

def validate_input(data: Dict[str, Any]) -> bool:
    """Validate all form fields"""
    if not all([
        isinstance(data.get('username'), str),
        isinstance(data.get('email'), str),
        isinstance(data.get('password'), str)
    ]):
        return False
    
    if not re.match(r'^[a-zA-Z0-9_]{3,50}$', data.get('username', '')):
        return False
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data.get('email', '')):
        return False
    
    if len(data.get('password', '')) < 8:
        return False
    
    return True

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Process form data securely
        data = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data
        }
        
        # Validate all inputs
        if not validate_input(data):
            return render_template('update_profile.html', form=form, error='Invalid input')
        
        # Here you would typically:
        # - Hash the password
        # - Update user database
        # - Set session variables
        
        return redirect(url_for('profile_success'))
    
    return render_template('update_profile.html', form=form)

@app.route('/profile_success')
def profile_success():
    """Success page after profile update"""
    return render_template('profile_success.html')