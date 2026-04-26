from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import timedelta
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

# Rate limiting to prevent brute force attacks
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Rate limiting for registration
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Sanitize and validate input
        username = form.username.data.strip()
        password = form.password.data
        
        # Validate username (alphanumeric, 3-50 chars)
        if not re.match(r'^[a-zA-Z0-9]{3,50}$', username):
            return render_template('register.html', form=form, error="Invalid username format")
        
        # Validate password strength
        if len(password) < 8 or len(password) > 16:
            return render_template('register.html', form=form, error="Password must be 8-16 characters")
        
        # Hash password securely
        hashed_password = generate_password_hash(password)
        
        # In a real app, you would save to database here
        # For this example, we'll just log the attempt
        logger.info(f"Registration attempt for user: {username}")
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/profile')
def profile():
    # In a real app, you would fetch the user's profile data here
    # For this example, we'll just return a generic message
    return "Welcome to your profile page!"

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production