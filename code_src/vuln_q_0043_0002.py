from flask import Flask, request, jsonify, send_file
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

app = Flask(__name__)
bcrypt = Bcrypt(app)
limiter = Limiter(app, key_func=get_remote_address)

# Simulated database (replace with actual database in production)
users = {}
password_reset_tokens = {}

@app.route('/request_password_reset', methods=['POST'])
@limiter.limit("5 per minute")
def request_password_reset():
    email = request.json.get('email')
    if not email or email not in users:
        return jsonify({"error": "Invalid email"}), 400
    
    token = secrets.token_urlsafe(32)
    expiration = int(time.time()) + 3600  # 1 hour expiration
    password_reset_tokens[token] = {'email': email, 'expiration': expiration}
    
    # Send email with reset link (implement secure email sending)
    send_reset_email(email, token)
    
    return jsonify({"message": "Password reset email sent"}), 200

@app.route('/reset_password', methods=['POST'])
@limiter.limit("5 per minute")
def reset_password():
    token = request.json.get('token')
    new_password = request.json.get('password')
    
    if not token or not new_password:
        return jsonify({"error": "Invalid token or missing password"}), 400
    
    if token not in password_reset_tokens or password_reset_tokens[token]['expiration'] < int(time.time()):
        return jsonify({"error": "Token expired"}), 400
    
    email = password_reset_tokens[token]['email']
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    users[email] = hashed_password
    
    del password_reset_tokens[token]
    
    return jsonify({"message": "Password reset successful"}), 200

def send_reset_email(email, token):
    sender_email = "your_email@example.com"
    receiver_email = email
    password = os.environ.get('EMAIL_PASSWORD')
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Password Reset"
    message.attach(MIMEText(f"Please use this link to reset your password: https://yourapp.com/reset_password?token={token}", "plain"))
    
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production