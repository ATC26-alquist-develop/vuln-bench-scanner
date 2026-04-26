from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
 return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
 if request.method == 'POST':
 name = request.form['name']
 email = request.form['email']
 password = request.form['password']
 # Save the user's information in a database
 return redirect(url_for('profile', name=name))
 else:
 return render_template('register.html')

@app.route('/profile/<name>')
def profile(name):
 # Retrieve the user's information from the database
 return render_template('profile.html', name=name)

if __name__ == '__main__':
 app.run()