```python
import bcrypt
import secrets
from flask import Flask, request, session, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate a secure random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use a secure database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Set session timeout

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.')
            return redirect('/register')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
            return redirect('/register')
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            session.clear()
            session['user_id'] = user.id
            session.permanent = True
            flash('Logged in successfully.')
            return redirect('/dashboard')
        else:
            flash('Invalid username or password.')
            return redirect('/login')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.')
        return redirect('/login')
    return render_template('dashboard.html')

if __name__ == '__main__':
    db.create_all()
    app.run(ssl_context='adhoc')  # Enable HTTPS
```


This implementation includes several security measures:

1. Password hashing using bcrypt, which is a secure hashing algorithm designed for password storage.
2. CSRF protection to prevent cross-site request forgery attacks.
3. Secure session management with HTTPS-only cookies and HTTP-only flag.
4. Session timeout to limit the duration of active sessions.
5. Input validation and sanitization to prevent injection attacks.
6. Use of parameterized queries to prevent SQL injection.
7. HTTPS enforcement to ensure encrypted communication.
8. Secure secret key generation for the Flask application.

Note that this code assumes you're using Flask and SQLAlchemy. You should also ensure that your production environment is properly configured with HTTPS, secure headers, and other security best practices. Additionally, consider implementing rate limiting, account lockout policies, and multi-factor authentication for enhanced security.