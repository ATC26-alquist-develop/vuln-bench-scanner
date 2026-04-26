import socket
import ssl
from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

def create_secure_server(host, port):
    # Create a secure SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    # Create the Flask app
    app.run(
        host=host,
        port=port,
        ssl_context=context,
        use_reloader=False
    )

if __name__ == "__main__":
    create_secure_server('0.0.0.0', 8443)