import socket
import ssl
from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    # Bind to localhost only
    app.run(host='127.0.0.1', port=8443)