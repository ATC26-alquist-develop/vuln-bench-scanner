from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)  # Generate a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session timeout in seconds

db = SQLAlchemy(app)

class Guestbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def before_request():
    if request.method == 'GET':
        session.permanent = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        
        # Input validation
        if not name or not message:
            return "Name and message are required", 400
        
        # Sanitize inputs
        name = re.sub(r'[^\w\s]', '', name)
        message = re.sub(r'<script>.*?</script>', '', message)
        
        # Check for XSS attempts
        if '<script>' in message:
            return "XSS attempt detected", 400
        
        # Check for CSRF
        if 'X-CSRF-Token' not in request.headers:
            return "CSRF token missing", 400
        
        # Store in database
        new_entry = Guestbook(name=name, message=message)
        db.session.add(new_entry)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    # Render form
    entries = Guestbook.query.order_by(Guestbook.timestamp.desc()).all()
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    db.create_all()
    app.run(ssl_context='adhoc')  # Enable HTTPS