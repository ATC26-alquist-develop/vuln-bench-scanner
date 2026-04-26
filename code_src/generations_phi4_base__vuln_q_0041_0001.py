from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy database to store user profiles
user_profiles = {
    'user1': {'name': 'John Doe', 'email': 'john@example.com'},
    'user2': {'name': 'Jane Smith', 'email': 'jane@example.com'}
}

@app.route('/')
def index():
    return render_template('index.html', profiles=user_profiles)

@app.route('/update_profile/<username>', methods=['GET', 'POST'])
def update_profile(username):
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')

        # Update the user profile
        user_profiles[username] = {'name': name, 'email': email}

        # Redirect to the profile page
        return redirect(url_for('index'))

    # Render the profile update form
    return render_template('update_profile.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)