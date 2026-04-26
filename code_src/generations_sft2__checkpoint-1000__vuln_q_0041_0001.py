from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure random secret key
app.config['WTF_CSRF_ENABLED'] = True  # CSRF protection

# Simulated database (replace with actual database in production)
users = {}

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField('Update Profile')

@app.route('/profile', methods=['GET', 'POST'])
def update_profile():
    form = ProfileForm()
    if 'username' in session:
        user = users.get(session['username'])
        if user:
            form.username.data = user['username']
            form.email.data = user['email']
            form.password.data = user['password']
            form.confirm_password.data = user['password']
    return render_template('profile.html', form=form)

@app.route('/profile', methods=['POST'])
def handle_profile_update():
    form = ProfileForm(request.form)
    if form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Validate password strength
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$', password):
            return render_template('profile.html', form=form, error='Password must be 12+ chars with letters, numbers, and special chars')
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Update user data (replace with actual database update logic)
        users[username] = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        
        # Clear form data
        session.pop('username', None)
        
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False in production