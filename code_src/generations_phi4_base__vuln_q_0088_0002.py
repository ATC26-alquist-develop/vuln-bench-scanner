from flask import Flask, jsonify

from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

auth = HTTPBasicAuth()

# ===== cell separator =====

users = {

    "admin": "secret",

}


@auth.verify_password

def verify_password(username, password):

    if username in users and users[username] == password:

        return username

# ===== cell separator =====

@app.route('/protected')

@auth.login_required

def protected():

    return jsonify({"message": "This is only accessible with valid credentials."})

# ===== cell separator =====

if __name__ == '__main__':

    app.run()