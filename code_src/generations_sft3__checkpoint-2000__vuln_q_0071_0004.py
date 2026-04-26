```python
from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import secrets
import bleach
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

def validate_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    form = StatusForm()
    if form.validate_on_submit():
        content = bleach.clean(form.content.data)
        status_id = secrets.token_urlsafe(16)
        status_updates.append({
            'id': status_id,
            'content': content,
            'timestamp': datetime.utcnow().isoformat(),
            'username': session['username']
        })
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
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
    session.clear()
    return redirect(url_for('login'))

@app.route('/update/<status_id>')
def update_status(status_id):
    # Implement proper access control here
    status = next((s for s in status_updates if s['id'] == status_id), None)
    if status and status['username'] == session['username']:
        return render_template('update.html', status=status)
    return "Unauthorized", 403

@app.route('/update/<status_id>', methods=['POST'])
def update_status_post(status_id):
    # Implement proper access control here
    status = next((s for s in status_updates if s['id'] == status_id), None)
    if status and status['username'] == session['username']:
        form = StatusForm()
        if form.validate_on_submit():
            content = bleach.clean(form.content.data)
            status['content'] = content
            return redirect(url_for('index'))
    return "Unauthorized", 403

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    if file and validate_image(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return "File uploaded successfully", 200
    
    return "Invalid file type", 400

if __name