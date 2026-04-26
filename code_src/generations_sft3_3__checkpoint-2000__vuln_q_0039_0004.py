import socket
import sys

def create_secure_socket():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind to all available interfaces
        server_address = ('0.0.0.0', 8080)
        sock.bind(server_address)
        
        # Listen for incoming connections (max 1 connection in queue)
        sock.listen(1)
        
        print(f"Listening on {server_address}")
        return sock
        
    except socket.error as msg:
        print(f"Failed to create socket: {msg}")
        sys.exit(1)