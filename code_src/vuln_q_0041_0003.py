from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import os
import logging

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        logging.warning(f"Attempted to delete non-existent account: {username}")
        return jsonify({'error': 'Account not found'}), 404

    if not check_password_hash(user.password_hash, password):
        logging.warning(f"Failed login attempt for account: {username}")
        return jsonify({'error': 'Invalid credentials'}), 401

    try:
        db.session.delete(user)
        db.session.commit()
        logging.info(f"Account deleted: {username}")
        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting account: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS