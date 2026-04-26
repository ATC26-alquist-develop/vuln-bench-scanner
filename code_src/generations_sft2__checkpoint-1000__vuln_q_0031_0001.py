from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.csrf import CSRFProtect
import secrets
import bcrypt
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate secure random key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout
csrf = CSRFProtect(app)

# Simulated database (replace with actual database in production)
users_db = {}

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    submit = SubmitField('Submit')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if user already exists
        if username in users_db:
            return "Username already exists", 400
            
        # Hash password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store user data (replace with database in production)
        users_db[username] = {
            'email': email,
            'password': hashed_password
        }
        
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Verify credentials (replace with database in production)
        if username in users_db and bcrypt.checkpw(password.encode('utf-8'), users_db[username]['password']):
            session['user'] = username
            session.permanent = True  # Use permanent session
            return redirect(url_for('profile'))
        return "Invalid credentials", 401
    
    return render_template('login.html', form=form)

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    # Fetch user data (replace with database in production)
    user_data = users_db.get(username, {})
    
    return render_template('profile.html', username=username, data=user_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False in production