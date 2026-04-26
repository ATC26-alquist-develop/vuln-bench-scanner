from flask import Flask, render_template, redirect, url_for, request, flash

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Change this to a random secret key


login_manager = LoginManager()

login_manager.init_app(app)


# User model

class User(UserMixin):

    def __init__(self, id, username, password):

        self.id = id

        self.username = username

        self.password = password


# In-memory user storage

users = []

@login_manager.user_loader

def load_user(user_id):

    for user in users:

        if user.id == user_id:

            return user

    return None


@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(len(users) + 1, username, hashed_password)

        users.append(new_user)

        flash('User registered successfully!')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        for user in users:

            if user.username == username and check_password_hash(user.password, password):

                login_user(user)

                flash('Logged in successfully!')

                return redirect(url_for('dashboard'))

        flash('Invalid username or password!')

    return render_template('login.html')


@app.route('/dashboard')

@login_required

def dashboard():

    return f'Welcome, {current_user.username}!'


@app.route('/logout')

@login_required

def logout():

    logout_user()

    return redirect(url_for('login'))


if __name__ == '__main__':

    app.run(debug=True)