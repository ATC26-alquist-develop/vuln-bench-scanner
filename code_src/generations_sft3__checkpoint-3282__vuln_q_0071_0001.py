from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import os
import secrets
import html
import time
from datetime import datetime, timedelta
import threading
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure logging
logging.basicConfig(filename='forum.log', level=logging.INFO)

# Configure Flask app with secure defaults
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Simulated database (replace with actual database in production)
messages = []
users = {}

class PostForm(FlaskForm):
    content = TextAreaField('Content', 
                           validators=[DataRequired(), Length(max=500)])

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    return html.escape(text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def post_message():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    form = PostForm()
    if form.validate_on_submit():
        content = sanitize_input(form.content.data)
        timestamp = datetime.now().isoformat()
        message_id = secrets.token_urlsafe(16)
        
        # Store message securely
        messages.append({
            'id': message_id,
            'username': session['username'],
            'content': content,
            'timestamp': timestamp
        })
        
        # Log activity
        logging.info(f"User {session['username']} posted message")
        
        return redirect(url_for('view_messages'))
    
    return render_template('post.html', form=form)

@app.route('/view')
def view_messages():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_messages = messages[start:end]
    
    return render_template('view.html', messages=paginated_messages)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # In production, validate against secure database
        if username and password == 'secure_password':
            session['username'] = username
            return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development