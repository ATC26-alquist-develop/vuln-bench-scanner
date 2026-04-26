from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import os
import secrets
import html
import time
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# In-memory storage (for demonstration purposes only)
# In production, use a secure database
messages = []
users = {}

class PostForm(FlaskForm):
    content = TextAreaField('Content', 
        validators=[DataRequired(), Length(max=500)])

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    return html.escape(text)

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    return render_template('index.html', form=PostForm())

@app.route('/post', methods=['POST'])
def post_message():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    form = PostForm()
    if form.validate_on_submit():
        content = sanitize_input(form.content.data)
        timestamp = time.time()
        message_id = secrets.token_hex(16)
        
        # Store message securely
        messages.append({
            'id': message_id,
            'username': session['username'],
            'content': content,
            'timestamp': timestamp
        })
        
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/view')
def view_messages():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Filter messages to show only for current user
    user_messages = [m for m in messages if m['username'] == session['username']]
    return render_template('view.html', messages=user_messages)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # In production, use secure password checking and proper database
    if username and password and username in users:
        if check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development