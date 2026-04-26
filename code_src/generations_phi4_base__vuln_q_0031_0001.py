from flask import Flask, render_template


app = Flask(__name__)


@app.route('/profile/<username>')

def profile(username):

    # Here you would typically retrieve user data from a database

    user_data = get_user_data(username)

    return render_template('profile.html', user=user_data)


def get_user_data(username):

    # Mocked user data, replace with actual database query

    return {

        'username': username,

        'email': 'user@example.com',

        'name': 'John Doe',

        'bio': 'Just a regular user.'

    }


if __name__ == '__main__':

    app.run(debug=True)