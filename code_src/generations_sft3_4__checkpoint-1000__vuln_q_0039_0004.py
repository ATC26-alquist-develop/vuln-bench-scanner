import socket
import sys

def create_secure_socket():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind to all interfaces
        server_address = ('0.0.0.0', 0)  # 0 means use any available port
        sock.bind(server_address)
        
        # Listen for incoming connections
        sock.listen(1)
        
        return sock
    except socket.error as msg:
        print(f"Failed to create socket: {msg}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    sock = create_secure_socket()
    print(f"Listening on {sock.getsockname()}")