from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate secure random key
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    reset_token = db.Column(db.String(128), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        # Validate input
        username = request.json.get('username')
        new_password = request.json.get('new_password')
        
        if not username or not new_password:
            return jsonify({"error": "Missing username or password"}), 400

        # Find user
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Generate secure token
        token = secrets.token_hex(32)
        expiry = datetime.datetime.utcnow() + timedelta(hours=1)

        # Update user with token
        user.reset_token = token
        user.reset_token_expiry = expiry
        db.session.commit()

        # Send reset link (implement secure email sending here)
        # ...

        return jsonify({"message": "Password reset instructions sent"}), 200

    except Exception as e:
        # Log error securely
        return jsonify({"error": "Internal server error"}), 500

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password_with_token(token):
    try:
        # Validate token
        user = User.query.filter_by(reset_token=token).first()
        if not user or user.reset_token_expiry < datetime.datetime.utcnow():
            return jsonify({"error": "Invalid or expired token"}), 400

        # Get new password
        new_password = request.json.get('new_password')
        
        if not new_password:
            return jsonify({"error": "Missing new password"}), 400

        # Hash new password
        hashed_password = generate_password_hash(new_password)

        # Update user password
        user.password_hash = hashed_password
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        return jsonify({"message": "Password reset successful"}), 200

    except Exception as e:
        # Log error securely
        return jsonify({"error": "Internal server error"}), 500