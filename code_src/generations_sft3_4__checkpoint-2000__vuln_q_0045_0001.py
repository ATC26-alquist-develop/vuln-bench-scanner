from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.csrf import CSRFProtect
import secrets
import bcrypt
import re
from datetime import timedelta
import logging
from typing import Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure secret key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

def is_valid_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,50}$', username))

def is_valid_password(password: str) -> bool:
    """Validate password strength."""
    return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password))

@app.before_request
def make_session_permanent():
    """Ensure session is permanent."""
    session.permanent = True

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if not is_valid_username(username) or not is_valid_password(password):
            return render_template('register.html', form=form, error="Invalid username or password format")
            
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # In a real application, you would save to database here
        # For this example, we're just logging
        logger.info(f"New user registered: {username}")
        
        return redirect(url_for('profile'))
    
    return render_template('register.html', form=form)

@app.route('/profile')
def profile():
    # In a real application, you would fetch the user's profile data here
    # For this example, we're just returning a generic message
    return render_template('profile.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production