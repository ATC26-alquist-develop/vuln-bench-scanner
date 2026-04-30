from functools import wraps
from typing import Dict, Optional
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta
import sqlite3
from contextlib import contextmanager

# Secure database connection
DB_PATH = 'users.db'

# Secure session configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Secure password policy
PASSWORD_MIN_LENGTH = 12
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$')

# Secure rate limiting
MAX_ATTEMPTS = 3
LOCKOUT_DURATION = timedelta(minutes=15)
login_attempts: Dict[str, Dict] = {}

@contextmanager
def get_db_connection():
    """Secure database connection context manager"""
    try:
        conn = sqlite3.connect(DB_PATH)
        yield conn
    finally:
        if conn:
            conn.close()

def init_db():
    """Initialize database with secure schema"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def is_rate_limited(username: str) -> bool:
    """Check if user is rate limited"""
    if username in login_attempts:
        attempts = login_attempts[username]
        if attempts['count'] >= MAX_ATTEMPTS:
            if datetime.now() - attempts['last_attempt'] < LOCKOUT_DURATION:
                return True
            else:
                attempts['count'] = 0
    return False

def update_login_attempt(username: str) -> None:
    """Update login attempt count"""
    if username in login_attempts:
        login_attempts[username]['count'] += 1
        login_attempts[username]['last_attempt'] = datetime.now()
    else:
        login_attempts[username] = {'count': 1, 'last_attempt': datetime.now()}

def login_required(f):
    """Secure login required decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return {'error': 'Authentication required'}, 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Input validation
        if not username or not password:
            return {'error': 'Username and password are required'}, 400

        # Validate username
        if not username or not isinstance(username, str) or not PASSWORD_PATTERN.match(username):
            return {'error': 'Invalid username'}, 400

        # Validate password
        if not isinstance(password, str) or not PASSWORD_PATTERN.match(password):
            return {'error': 'Invalid password'}, 400

        # Check if user already exists
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                return {'error': 'Username already exists'}, 409

        # Hash password with salt
        password_hash = generate_password_hash(password)

        # Store user securely
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',