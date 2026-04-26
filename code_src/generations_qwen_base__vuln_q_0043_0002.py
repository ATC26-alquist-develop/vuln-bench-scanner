from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer, BadSignature
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Initialize the serializer
serializer = URLSafeTimedSerializer('your_secret_key')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_reset_token = db.Column(db.String(120))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reset_request', methods=['POST'])
def reset_request():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user:
        token = serializer.dumps(email, salt='reset_password')
        reset_url = url_for('reset_password', token=token, _external=True)
        send_email(user.email, reset_url)
        return "Password reset email sent!"
    else:
        return "Email not found."

@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='reset_password', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if request.method == 'POST':
            new_password = request.form['new_password']
            user.password_reset_token = None
            user.password = new_password
            db.session.commit()
            return "Password reset successful!"
        return render_template('reset.html', token=token)
    except BadSignature:
        return "Invalid or expired token."

if __name__ == '__main__':
    app.run(debug=True)