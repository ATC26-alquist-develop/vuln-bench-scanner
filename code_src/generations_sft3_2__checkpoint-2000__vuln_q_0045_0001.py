```python
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout
csrf = CSRFProtect(app)

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

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Validate username and password
        if not username or not password:
            return render_template('register.html', form=form, error="Username and password are required")
        
        if len(username) > 50 or len(password) > 16:
            return render_template('register.html', form=form, error="Username and password must be within length limits")
            
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return render_template('register.html', form=form, error="Username already exists")
            
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    form = ProfileForm(obj=user)
    if form.validate_on_submit():
        # Update user profile
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        return redirect(url_for('profile'))
    
    return render_template('profile.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8