from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import secrets
import time
import html
import re
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Simulated database (replace with actual database in production)
status_updates = []
users = {}

class StatusForm(FlaskForm):
    content = TextAreaField('Status', validators=[
        DataRequired(),
        Length(max=280)
    ])

def is_valid_username(username):
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def is_valid_content(content):
    return len(content) <= 280 and len(content) > 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        form = StatusForm()
        if form.validate_on_submit():
            content = form.content.data
            if is_valid_content(content):
                status = {
                    'content': content,
                    'timestamp': datetime.utcnow().isoformat(),
                    'username': session['username']
                }
                status_updates.append(status)
                return redirect(url_for('index'))
            else:
                return render_template('index.html', form=form, error="Invalid status")
        
        return render_template('index.html', form=form)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            # In production, validate against secure database
            if is_valid_username(username) and password == os.environ.get('APP_PASSWORD'):
                session['username'] = username
                return redirect(url_for('index'))
        
        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/user/<username>')
def user_feed(username):
    if not is_valid_username(username):
        return "Invalid username", 400
    
    user_feed = [s for s in status_updates if s['username'] == username]
    return render_template('user_feed.html', username=username, feed=user_feed)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return "File uploaded successfully", 200
    
    return "Invalid file type", 400

if __name__ == '__main__':
    app.run(debug=False)