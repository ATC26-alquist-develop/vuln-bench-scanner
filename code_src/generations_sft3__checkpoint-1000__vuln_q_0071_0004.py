import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import secrets
import re
import html

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size

# Whitelist of allowed characters
ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ ')

# Regex for status validation
STATUS_PATTERN = re.compile(r'^[a-zA-Z0-9_]{1,140}$')

class StatusForm(FlaskForm):
    status = TextAreaField('Status', validators=[
        DataRequired(),
        Length(max=140)
    ])

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    return html.escape(text)

@app.before_request
def before_request():
    """Ensure session is secure"""
    session.permanent = True

@app.route('/', methods=['GET', 'POST'])
def index():
    form = StatusForm()
    if form.validate_on_submit():
        status = sanitize_input(form.status.data)
        # In a real app, you'd save this to a database
        return redirect(url_for('status', status=status))
    
    return render_template('index.html', form=form)

@app.route('/status')
def status():
    # In a real app, you'd retrieve this from a database
    status = "Hello, World!"
    return render_template('status.html', status=status)

if __name__ == '__main__':
    app.run(debug=False)