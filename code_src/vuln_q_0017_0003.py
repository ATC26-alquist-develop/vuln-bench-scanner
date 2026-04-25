from flask import Flask, request, make_response, session
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import secrets
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Implement secure authentication here
        # For example, verify username and password against a database
        # Use parameterized queries to prevent SQL injection
        # Implement proper password hashing
        # Use secure session management
        session['user_id'] = 'user123'  # Example user ID
        return 'Login successful'
    return render_template('login.html', form=form)

@app.route('/track_visit')
def track_visit():
    if 'user_id' not in session:
        return 'Unauthorized', 401
    
    # Generate a secure, random token
    visit_token = secrets.token_urlsafe(32)
    
    # Store token securely (e.g., in database)
    # For demonstration, we'll just return it
    return f'Visit token: {visit_token}'

@app.route('/verify_visit', methods=['POST'])
def verify_visit():
    if 'user_id' not in session:
        return 'Unauthorized', 401
    
    token = request.form.get('token')
    if not token:
        return 'Invalid token', 400
    
    # Verify token against stored value
    # In production, use secure database lookup
    if token == 'example_token':
        return 'Visit verified'
    else:
        return 'Invalid token', 400

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS