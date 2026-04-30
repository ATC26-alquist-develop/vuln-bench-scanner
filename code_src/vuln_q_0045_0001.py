```python
from flask import Flask, request, render_template, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
import os
import secrets
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure secret key generation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use environment variables in production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes session timeout

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=3, max=80), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=120), validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8)])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            return "Username already exists", 400
        
        new_user = User(username=form.username.data, email=form.email.data)
        # Use secure password hashing
        new_user.password_hash = generate_secure_password_hash(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and verify_password(form.password.data, user.password_hash):
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        return "Invalid credentials", 401
    return render_template('login.html', form=form)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        abort(403)  # Forbidden access
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

def generate_secure_password_hash(password):
    # Use a secure password hashing algorithm like bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    # Verify password against hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

if __name__ == '__main__':
    db.create_all()
    app.run(ssl_context='adhoc')  # Use HTTPS in development
```