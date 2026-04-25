from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from werkzeug.exceptions import Forbidden
from typing import List, Dict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Use a strong, unique secret key in production
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    """
    Returns a list of all registered users.
    Only accessible to authenticated users.
    """
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@app.errorhandler(Forbidden)
def handle_forbidden(e):
    """
    Handles 403 Forbidden errors.
    """
    return jsonify(error="Access denied"), 403