from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import CSRFProtect
from wtforms import StringField
from wtforms.validators import DataRequired, Length
import secrets
import time
import re
from datetime import datetime, timedelta
import html

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# In-memory storage (replace with database in production)
status_updates = []
user_sessions = {}

class StatusForm:
    def __init__(self):
        self.name = StringField('Status', 
            validators=[DataRequired(), Length(max=280)])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = StatusForm()
        if form.validate_on_submit():
            # Sanitize input
            status = html.escape(form.name.data[:280])
            
            # Check for existing status
            if any(s['status'] == status for s in status_updates):
                return "Status already exists", 400
            
            # Create new status
            status_id = secrets.token_hex(16)
            status_time = datetime.utcnow()
            status_updates.append({
                'id': status_id,
                'status': status,
                'created_at': status_time,
                'updated_at': status_time
            })
            
            # Create user session
            session['user_id'] = secrets.token_hex(16)
            user_sessions[session['user_id']] = {
                'created_at': datetime.utcnow(),
                'last_activity': datetime.utcnow()
            }
            
            return redirect(url_for('index'))
    
    # Get user session
    user_id = session.get('user_id')
    if user_id:
        user_data = user_sessions.get(user_id)
        if user_data and (datetime.utcnow() - user_data['last_activity']) < timedelta(minutes=5):
            # User is active, update last activity
            user_sessions[user_id]['last_activity'] = datetime.utcnow()
            return render_template('index.html', 
                status_updates=status_updates, 
                user_id=user_id)
    
    # No session or inactive user, redirect to login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Implement secure login logic here
        # For example, validate credentials against a secure database
        # and create a new session
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development