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

class ProfileForm(FlaskForm):
    name = StringField('Name', 
                       validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', 
                        validators=[DataRequired(), Length(max=100)])

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Rate limiting for registration
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Validate username and password
        if not re.match(r'^[a-zA-Z0-9_]{3,50}$', username):
            return render_template('register.html', form=form, error="Invalid username format")
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return render_template('register.html', form=form, error="Invalid password format")
        
        # In a real application, you would hash the password here
        # and store it in a database
        return redirect(url_for('profile'))
    
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('register'))
    
    form = ProfileForm()
    if form.validate_on_submit():
        # In a real application, you would update the user's profile here
        # and store it in a database
        return redirect(url_for('profile'))
    
    return render_template('profile.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Rate limiting for login
def login():
    # Implement secure login logic here
    # For example, validate credentials against a database
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development