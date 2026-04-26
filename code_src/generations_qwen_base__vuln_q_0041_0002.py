from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # A secret key for session management
bcrypt = Bcrypt(app)

# Dummy user data (for demonstration purposes)
users = {
    'user1': {'password': 'password123'},
    'user2': {'password': 'securepassword456'}
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        # Check if the user is in the database
        if username in users and bcrypt.check_password_hash(users[username]['password'], old_password):
            # Hash the new password
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            users[username]['password'] = hashed_password
            flash('Password changed successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect old password or user not found.', 'danger')
            return redirect(url_for('home'))

    return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True)