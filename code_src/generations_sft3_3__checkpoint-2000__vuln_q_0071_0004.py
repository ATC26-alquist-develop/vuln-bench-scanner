from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CSRFProtect
import secrets
import bleach
import re
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Secure secret key generation
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Secure CSRF protection
csrf = CSRFProtect(app)

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "20 per hour"]
)

class StatusForm(FlaskForm):
    status = TextAreaField('Status', 
        validators=[DataRequired(), Length(max=280, message='Status must be 1-280 characters')])

class UserForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(max=30, message='Username must be 1-30 characters')])

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def index():
    form = StatusForm()
    if form.validate_on_submit():
        # Sanitize and validate status
        status = bleach.clean(form.status.data)
        if len(status) <= 280:
            # Generate unique ID
            status_id = secrets.token_urlsafe(16)
            # Store status in database (implementation omitted for brevity)
            # ...
            return redirect(url_for('index'))
        else:
            form.status.errors.append('Status must be 1-280 characters')
    
    # Fetch user's status (implementation omitted for brevity)
    user_status = None
    
    return render_template('index.html', form=form, user_status=user_status)

@app.route('/user/<username>')
@limiter.limit("30 per minute")
def user_profile(username):
    # Implement user profile logic (implementation omitted for brevity)
    return "User profile page"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development