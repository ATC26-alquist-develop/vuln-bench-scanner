from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy data to store user profiles
profiles = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_profile', methods=['POST'])
def update_profile():
    username = request.form['username']
    new_email = request.form['email']
    new_phone = request.form['phone']
    
    # Update the profile
    profiles[username] = {'email': new_email, 'phone': new_phone}
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)