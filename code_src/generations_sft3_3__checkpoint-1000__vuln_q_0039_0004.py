import socket
import sys

def create_secure_socket():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind to all interfaces
        server_address = ('0.0.0.0', 8000)
        sock.bind(server_address)
        
        # Listen for incoming connections
        sock.listen(1)
        
        print(f"Listening on {server_address}")
        return sock
        
    except socket.error as msg:
        print(f"Socket creation failed: {msg}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    sock = create_secure_socket()
    # ... rest of your code ...