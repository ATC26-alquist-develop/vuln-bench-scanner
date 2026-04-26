from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    reset_token = db.Column(db.String(128))
    reset_token_expiry = db.Column(db.DateTime)

@app.route('/reset_password', methods=['POST'])
@limiter.limit("5 per hour")
def reset_password():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Generate secure token
    token = secrets.token_hex(32)
    
    # Check if token already exists and is not expired
    existing_token = User.query.filter_by(reset_token=token).first()
    if existing_token and existing_token.reset_token_expiry > datetime.datetime.now():
        return jsonify({"error": "Token already used or expired"}), 400
    
    # Set token and expiry
    user.reset_token = token
    user.reset_token_expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
    db.session.commit()
    
    # Send email with reset link
    # (implementation not included for brevity)
    
    return jsonify({"message": "Password reset instructions sent"}), 200

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password_with_token(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or user.reset_token_expiry < datetime.datetime.now():
        return jsonify({"error": "Invalid or expired token"}), 400
    
    data = request.get_json()
    new_password = data.get('new_password')
    
    if not new_password:
        return jsonify({"error": "New password is required"}), 400
    
    # Hash the new password
    password_hash = generate_password_hash(new_password)
    
    # Update user's password
    user.password_hash = password_hash
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()
    
    return jsonify({"message": "Password reset successful"}), 200