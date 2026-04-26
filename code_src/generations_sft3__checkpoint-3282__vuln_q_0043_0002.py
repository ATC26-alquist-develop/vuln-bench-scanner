I'll help you implement a secure password reset feature. Before we dive into the code, let's discuss the security considerations:

1. Password reset tokens should be secure and time-limited
2. Passwords should be hashed using strong algorithms
3. The process should include email verification
4. We should use HTTPS for all communications
5. Implement proper input validation

Here's a secure implementation using Python with Flask:

```python
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
from email_validator import validate_email, EmailNotValidError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    reset_token = db.Column(db.String(120))
    reset_token_expiry = db.Column(db.DateTime)

@app.route('/reset_password', methods=['POST'])
def request_reset():
    try:
        email = validate_email(request.json.get('email')).email
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    token = secrets.token_hex(32)
    expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
    
    user.reset_token = token
    user.reset_token_expiry = expiry
    db.session.commit()

    # Send email with reset link
    reset_link = f"https://yourdomain.com/reset_password/{token}"
    msg = Message('Password Reset Request', sender='noreply@yourdomain.com', recipients=[email])
    msg.body = f"Click the following link to reset your password: {reset_link}"
    mail.send(msg)

    return jsonify({'message': 'Password reset instructions sent to your email'}), 200

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    try:
        token = validate_token(token)
    except:
        return jsonify({'error': 'Invalid or expired token'}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 400

    if datetime.datetime.now() > user.reset_token_expiry:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'error': 'Token expired. Request new password reset.'}), 400

    password = request.json.get('password')
    if not password or len(password) < 12:
        return jsonify({'error': 'Password must be at least 12 characters long'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    user.password_hash = hashed_password
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 20