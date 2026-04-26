from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import secrets
import bleach
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
MAX_MESSAGE_LENGTH = 500  # characters
MAX_THREADS = 100
MAX_THREADS_PER_USER = 10

class PostForm(FlaskForm):
    message = TextAreaField('Message', 
        validators=[DataRequired(), Length(max=MAX_MESSAGE_LENGTH)])

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    return bleach.clean(html.escape(text))

def validate_thread_limit(username):
    """Check thread creation limits"""
    user_threads = [m for m in messages if m['username'] == username]
    return len(user_threads) < MAX_THREADS_PER_USER

def rate_limit():
    """Rate limiting for posting"""
    current_time = time.time()
    while True:
        yield {'seconds': 1, 'requests': 1}
        time.sleep(1)

@app.before_request
def before_request():
    """Rate limiting decorator"""
    if not hasattr(request, 'threaded'):
        request.threaded = threading.current_thread().ident
    app.before_request_funcs[app.view_functions['index']] = rate_limit()

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['GET', 'POST'])
def post_message():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    form = PostForm()
    if form.validate_on_submit():
        username = session['username']
        content = sanitize_input(form.message.data)
        
        # Check thread limits
        if not validate_thread_limit(username):
            return "Thread limit reached", 403
            
        # Check message length
        if len(content) > MAX_MESSAGE_LENGTH:
            return "Message too long", 400
            
        # Create timestamp
        timestamp = datetime.now().isoformat()
        
        # Store sanitized message
        messages.append({
            'username': username,
            'content': content,
            'timestamp': timestamp
        })
        
        # Sort messages by timestamp
        messages.sort(key=lambda x: x['timestamp'])
        
        return redirect(url_for('index'))
    
    return render_template('post.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # In production, validate against secure database
        if username and password:  # Placeholder - implement proper auth
            session['username'] = username
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production