from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
    # Check if the user has visited before
    if 'visits' in request.cookies:
        visits = int(request.cookies.get('visits')) + 1
    else:
        visits = 1

    # Set the number of visits in the cookie
    resp = make_response(f'You have visited this page {visits} times.')
    resp.set_cookie('visits', str(visits))

    return resp

if __name__ == '__main__':
    app.run()