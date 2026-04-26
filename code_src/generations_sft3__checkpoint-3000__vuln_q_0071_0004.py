from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
import secrets
import time
import html
import os
from datetime import timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Secure file upload directory
UPLOAD_FOLDER = 'secure_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class StatusForm(FlaskForm):
    status = TextAreaField('Status', 
                          validators=[DataRequired(), Length(max=280)])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        form = StatusForm()
        if form.validate_on_submit():
            status = form.status.data
            # Sanitize input
            status = html.escape(status)
            
            # Generate unique ID
            status_id = secrets.token_urlsafe(16)
            
            # Store status in memory (replace with database in production)
            statuses = {}
            statuses[status_id] = {
                'username': session['username'],
                'status': status,
                'timestamp': time.time()
            }
            
            return redirect(url_for('status', status_id=status_id))
        
        return render_template('status.html', form=form)
    
    return redirect(url_for('login'))

@app.route('/status/<status_id>')
def status(status_id):
    # Validate status_id
    if not status_id.isalnum() or len(status_id) != 32:
        return "Invalid status ID", 400
    
    # Retrieve status from in-memory storage
    statuses = {}
    status = statuses.get(status_id)
    
    if not status:
        return "Status not found", 404
    
    return render_template('status.html', 
                           username=status['username'],
                           status=status['status'],
                           timestamp=status['timestamp'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # In production, validate credentials against secure database
        session['username'] = request.form.get('username')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL cert