import socket
import sys

def create_secure_server(host='0.0.0.0', port=8000):
    try:
        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set SO_REUSEADDR option to avoid "Address already in use" errors
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the host and port
        server_socket.bind((host, port))
        
        # Listen for incoming connections (max 5 queued connections)
        server_socket.listen(5)
        
        print(f"Server listening on {host}:{port}")
        return server_socket
        
    except socket.error as e:
        print(f"Error creating server socket: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

# Usage example
if __name__ == "__main__":
    server = create_secure_server()
    # ... rest of your server code ...