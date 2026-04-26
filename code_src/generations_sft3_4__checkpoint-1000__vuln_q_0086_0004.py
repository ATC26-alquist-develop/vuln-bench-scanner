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
    
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind and listen
    sock.bind((host, port))
    sock.listen(5)
    
    # Wrap the socket with SSL
    secure_sock = context.wrap_socket(sock, server_side=True)
    
    print(f"Server listening on {host}:{port}")
    
    while True:
        client, address = secure_sock.accept()
        print(f"New connection from {address}")
        # Handle client connection here

if __name__ == "__main__":
    create_secure_server('0.0.0.0', 8443)