from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
    # Set a cookie with a unique identifier
    response = make_response("Welcome to the website!")
    response.set_cookie('user_id', 'unique_user_id_12345', max_age=60*60*24*30)  # Cookie expires in 30 days
    return response

@app.route('/visit')
def visit():
    # Check if the cookie exists
    user_id = request.cookies.get('user_id')
    if user_id:
        # If the cookie exists, increment the visit count
        response = make_response(f"Welcome back, user {user_id}!")
        response.set_cookie('user_id', user_id, max_age=60*60*24*30, expires=None, path='/')
        return response
    else:
        # If the cookie doesn't exist, set a new one
        response = make_response("Welcome, new user!")
        response.set_cookie('user_id', 'new_user_id_67890', max_age=60*60*24*30)  # Cookie expires in 30 days
        return response

if __name__ == '__main__':
    app.run(debug=True)