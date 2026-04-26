I'll help you implement a secure password reset feature. Before we dive into the code, let me explain the security considerations:

1. Password reset tokens should be short-lived
2. Tokens should be cryptographically secure
3. Passwords should be hashed before storage
4. The reset process should be rate-limited
5. The reset link should expire after a certain time

Here's a secure implementation using Flask and SQLAlchemy:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['RESET_TOKEN_EXPIRATION'] = 3600  # 1 hour
app.config['RATE_LIMIT'] = 5  # requests per minute

db = SQLAlchemy(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    reset_token = db.Column(db.String(64), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

@app.route('/reset_password', methods=['POST'])
@limiter.limit("10 per minute")
def reset_password():
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Generate a new reset token
    reset_token = secrets.token_hex(32)
    expiry = datetime.utcnow() + timedelta(hours=app.config['RESET_TOKEN_EXPIRATION'])
    
    # Update user's reset token
    user.reset_token = reset_token
    user.reset_token_expiry = expiry
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Failed to reset password"}), 500
    
    # Send reset link to user's email (implementation not shown)
    # For security, this should be done via email verification
    
    return jsonify({"message": "Password reset link sent"}), 200

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password_with_token(token):
    try:
        user = User.query.filter_by(reset_token=token).first()
        if not user or user.reset_token_expiry < datetime.utcnow():
            return jsonify({"error": "Invalid or expired reset token"}), 400
        
        new_password = request.json.get('new_password')
        if not new_password:
            return jsonify({"error": "New password is required"}), 400
        
        # Hash the new password
        hashed_password = generate_password_hash(new_password)
        
        # Update user's password
        user.password_hash = hashed_password
        user.reset_token = None
        user.reset_token_expiry = None
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Failed to reset password"}), 500
        
        return jsonify({"message": "Password reset successful"}), 200
    
    except Exception as e:
        return jsonify({"error": "An error occurred