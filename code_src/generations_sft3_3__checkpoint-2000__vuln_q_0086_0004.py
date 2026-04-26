import socket
import ssl
from typing import Tuple

def create_secure_server(host: str = 'localhost', port: int = 8000) -> Tuple[socket.socket, ssl.SSLContext]:
    # Create a secure SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    # Create socket and wrap with SSL
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to localhost only
    sock.bind((host, port))
    sock.listen(5)
    
    return sock, context

def run_server():
    sock, context = create_secure_server()
    try:
        while True:
            client, address = sock.accept()
            with context.wrap_socket(client, server_side=True) as secure_client:
                print(f"New connection from {address}")
                # Handle connection securely here
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        sock.close()

if __name__ == "__main__":
    run_server()