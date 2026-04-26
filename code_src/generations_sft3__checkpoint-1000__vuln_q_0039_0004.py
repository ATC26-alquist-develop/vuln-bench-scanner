import socket
import sys

def create_secure_socket():
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set SO_REUSEADDR to allow address reuse
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to all interfaces
        sock.bind(('0.0.0.0', 0))  # 0 is a placeholder for the actual port
        
        # Get the actual port number
        sock.listen(5)
        
        # Get the actual port number
        port = sock.getsockname()[1]
        
        print(f"Socket bound to port {port}")
        
        return sock
        
    except socket.error as e:
        print(f"Socket error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sock = create_secure_socket()
    # Further code to handle connections would go here