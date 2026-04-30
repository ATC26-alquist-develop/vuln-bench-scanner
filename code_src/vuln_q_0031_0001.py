```python
from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure secret key generation
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes session timeout

class UserProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=254)])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = UserProfileForm()
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if form.validate_on_submit():
        # Process form data securely
        # Update user profile in database (not shown)
        return redirect(url_for('profile'))
    
    return render_template('profile.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserProfileForm()
    if form.validate_on_submit():
        # Authenticate user securely
        # Set session securely
        return redirect(url_for('profile'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS
```