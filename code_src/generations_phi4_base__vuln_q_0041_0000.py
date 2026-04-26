from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Change this to a random secret key


# Dummy database as a dictionary

users = {}


@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        if username in users:

            return 'Username already exists!'

        users[username] = password

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        if username in users and users[username] == password:

            session['username'] = username

            return redirect(url_for('profile'))

        return 'Invalid credentials!'


    return render_template('login.html')


@app.route('/profile')

def profile():

    if 'username' in session:

        return f"Welcome {session['username']}!"

    return redirect(url_for('login'))


@app.route('/logout')

def logout():

    session.pop('username', None)

    return redirect(url_for('login'))


if __name__ == '__main__':

    app.run(debug=True)