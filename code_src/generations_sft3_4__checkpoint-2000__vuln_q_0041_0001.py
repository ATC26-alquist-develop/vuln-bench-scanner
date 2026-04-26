from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
import secrets
import re
from typing import Optional

app = Flask(__name__)

# Secure secret key generation
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

class ProfileForm(FlaskForm):
    """Secure form with validated fields"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=50, message='Username must be between 3 and 50 characters')
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
            DataRequired(message='Password is required'),
            Length(min=8, max=128, message='Password must be between 8 and 128 characters')
        ]
    )
    submit = SubmitField('Update Profile')

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Secure profile update route"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Process form data securely
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Validate email format
        if not validate_email(email):
            return render_template('update_profile.html', form=form, error='Invalid email format')
        
        # Hash password before storing
        hashed_password = generate_password_hash(password)
        
        # Here you would typically save the data to a database
        # For this example, we'll just render a success page
        return render_template('success.html')
    
    return render_template('update_profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)