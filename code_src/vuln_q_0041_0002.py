from flask import Flask, request, render_template, redirect, url_for, session
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key'  # Change this to a secure random key
login_manager = LoginManager(app)

# Simulated user database (replace with a real database in production)
users = {
    'user@example.com': {
        'password': generate_password_hash('securepassword123')
    }
}

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not all([old_password, new_password, confirm_password]):
            return render_template('change_password.html', error='All fields are required')
        
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', new_password):
            return render_template('change_password.html', error='Password must be 8-20 characters long and contain at least one letter and one number')
        
        if new_password != confirm_password:
            return render_template('change_password.html', error='Passwords do not match')
        
        if check_password_hash(users[current_user.email]['password'], old_password):
            users[current_user.email]['password'] = generate_password_hash(new_password)
            return redirect(url_for('profile'))
        else:
            return render_template('change_password.html', error='Invalid old password')
    
    return render_template('change_password.html')

@app.route('/profile')
@login_required
def profile():
    return f"Welcome to your profile, {current_user.email}!"