from flask import Flask, render_template, redirect, url_for, request, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Sample user data
users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/')
def home():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)