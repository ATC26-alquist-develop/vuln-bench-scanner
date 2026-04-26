from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
import secrets
import re
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

class ProfileForm(FlaskForm):
    """Secure form with validated fields"""
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
            DataRequired(message='Password is required'),
            Length(min=8, max=128, message='Password must be 8-128 characters')
        ]
    )
    submit = SubmitField('Update Profile')

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Secure profile update route"""
    if not session.get('user_id'):
        return redirect(url_for('login'))

    form = ProfileForm()
    
    # Validate form data
    if form.validate_on_submit():
        # Sanitize and validate input
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data
        
        # Additional validation
        if not re.match(r"^[a-zA-Z0-9]{3,50}$", username):
            form.username.errors.append("Invalid username format")
            return render_template('update_profile.html', form=form)
            
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            form.email.errors.append("Invalid email format")
            return render_template('update_profile.html', form=form)
            
        if len(password) < 8:
            form.password.errors.append("Password must be at least 8 characters")
            return render_template('update_profile.html', form=form)
            
        # Update user data (implement secure database update here)
        # ...
        
        return redirect(url_for('profile'))
    
    return render_template('update_profile.html', form=form)

@app.route('/profile')
def profile():
    """Secure profile view"""
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('profile.html')