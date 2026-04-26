from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import secrets
import time
from datetime import datetime
import html
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Simulated database (replace with actual database in production)
status_updates = []
users = {}

class StatusForm(FlaskForm):
    status = TextAreaField('Status', validators=[
        DataRequired(),
        Length(max=280)
    ])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        form = StatusForm()
        if form.validate_on_submit():
            status = form.status.data
            status = html.escape(status)  # Sanitize input
            timestamp = datetime.now().isoformat()
            status_id = secrets.token_hex(16)
            
            # Store status update
            status_updates.append({
                'id': status_id,
                'username': session['username'],
                'status': status,
                'timestamp': timestamp
            })
            
            return redirect(url_for('index'))
        
        return render_template('index.html', form=form)
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # In production, validate against secure database
        if username and password:  # Basic auth for demo
            users[username] = True
            session['username'] = username
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/status/<status_id>')
def view_status(status_id):
    # Implement proper access control
    for update in status_updates:
        if update['id'] == status_id:
            return render_template('status.html', update=update)
    return "Status not found", 404

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
        return "File uploaded successfully"
    
    return "Invalid file type", 400

if __name__ == '__main__':
    app.run(debug=False)