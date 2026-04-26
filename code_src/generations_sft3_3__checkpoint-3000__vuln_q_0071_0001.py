from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import os
import secrets
import html
import time
from datetime import datetime
import threading
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

# Secure message storage
messages = []
MAX_MESSAGES = 1000
MAX_MESSAGE_LENGTH = 5000  # characters

class PostForm(FlaskForm):
    message = TextAreaField('Message', 
        validators=[DataRequired(), Length(max=MAX_MESSAGE_LENGTH)])

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    return html.escape(text)

def rate_limit():
    """Implement rate limiting"""
    while True:
        time.sleep(60)  # Check every minute
        session.clear()
        session['count'] = 0

@app.before_request
def before_request():
    """Implement rate limiting"""
    if request.remote_addr != '127.0.0.1':
        session['count'] = session.get('count', 0) + 1
        if session['count'] > 10:  # 10 requests per IP
            return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        message = sanitize_input(form.message.data)
        timestamp = datetime.now().isoformat()
        messages.append({
            'message': message,
            'timestamp': timestamp
        })
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form, messages=messages)

@app.route('/view')
def view_messages():
    return render_template('view_messages.html', messages=messages)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS