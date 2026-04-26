import socket
import ssl
from typing import Tuple

def create_secure_server(host: str = '0.0.0.0', port: int = 8080) -> Tuple[socket.socket, ssl.SSLContext]:
    # Create a secure SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    # Create socket and wrap with SSL
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind and listen
    sock.bind((host, port))
    sock.listen(5)
    
    return sock, context

def run_server():
    try:
        sock, context = create_secure_server()
        print(f"Server listening on {sock.getsockname()}")
        
        while True:
            client, address = sock.accept()
            ssl_client = context.wrap_socket(client, server_side=True)
            print(f"Accepted connection from {address}")
            
            # Handle client connection here
            ssl_client.close()
            client.close()
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()