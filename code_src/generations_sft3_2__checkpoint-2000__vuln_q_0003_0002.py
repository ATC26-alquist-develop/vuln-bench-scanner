from flask import Flask, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta
import logging
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Configure secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup (using SQLAlchemy with parameterized queries)
Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    reset_token = Column(String(64), unique=True, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

# Rate limiting decorator
def rate_limit(max_requests: int, window: int):
    def decorator(f):
        requests = {}
        def wrapper(*args, **kwargs):
            now = datetime.utcnow()
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            
            if client_ip in requests:
                request_count, first_request = requests[client_ip]
                if now - first_request > timedelta(seconds=window):
                    requests[client_ip] = (1, now)
                elif request_count >= max_requests:
                    abort(429)  # Too Many Requests
                else:
                    requests[client_ip] = (request_count + 1, first_request)
            else:
                requests[client_ip] = (1, now)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/reset_password', methods=['POST'])
@rate_limit(max_requests=5, window=300)  # 5 requests per 5 minutes
def reset_password():
    try:
        # Input validation
        data = request.get_json()
        if not data or 'username' not in data or 'new_password' not in data:
            abort(400)  # Bad Request

        username = data['username']
        new_password = data['new_password']

        # Validate username format
        if not re.match(r'^[a-zA-Z0-9_]{3,50}$', username):
            abort(400)  # Bad Request

        # Validate password strength
        if len(new_password) < 12:
            abort(400)  # Bad Request

        # Find user
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        session.close()

        if not user:
            abort(404)  # Not Found

        # Generate secure token
        token = secrets.token_hex(32)
        expiry = datetime.utcnow() + timedelta(hours=1)

        # Update user with token
        user.reset_token = token
        user.reset_token_expiry = expiry
        session = Session()
        session.commit()
        session.close()

        # Send reset email (implementation not shown)
        # ...

        return jsonify({
            'message': 'Password reset instructions sent. Please check your email.',
            'token': token,
            'expiry': expiry.isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        abort(500)  # Internal Server Error

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production