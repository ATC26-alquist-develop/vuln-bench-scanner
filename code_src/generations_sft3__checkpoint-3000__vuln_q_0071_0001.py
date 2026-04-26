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
    """Rate limiting decorator"""
    last_request_times = {}
    while True:
        current_time = time.time()
        for client_id in list(last_request_times.keys()):
            if current_time - last_request_times[client_id] > 1:
                del last_request_times[client_id]
        time.sleep(0.1)

@app.before_request
def check_rate_limit():
    """Implement rate limiting"""
    client_id = request.headers.get('X-Forwarded-For') or request.remote_addr
    if client_id in last_request_times:
        current_time = time.time()
        if current_time - last_request_times[client_id] < 1:
            return redirect(url_for('index'))
    last_request_times[client_id] = time.time()

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
    # Run in production mode
    app.run(host='127.0.0.1', port=5000, debug=False)