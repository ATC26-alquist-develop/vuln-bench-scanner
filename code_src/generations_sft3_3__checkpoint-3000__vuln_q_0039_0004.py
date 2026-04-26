import socket
import sys

def create_secure_server(host='0.0.0.0'):
    try:
        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set SO_REUSEADDR option to avoid "Address already in use" errors
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to all interfaces
        server_socket.bind((host, 0))
        
        # Get the new port number
        server_port = server_socket.getsockname()[1]
        
        print(f"Server started on port {server_port}")
        return server_socket
        
    except socket.error as e:
        print(f"Failed to create server socket: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

# Usage example
if __name__ == "__main__":
    server = create_secure_server()
    # Listen for connections
    server.listen(5)
    # Accept connections
    # ...