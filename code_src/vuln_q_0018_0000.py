```python
import socket
import ssl
import certifi
from typing import Optional

def secure_connect(host: str, port: int, timeout: int = 10) -> Optional[socket.socket]:
    """
    Establish a secure SSL/TLS connection to a remote server.
    
    Args:
        host: The hostname or IP address of the server
        port: The port number to connect to
        timeout: Connection timeout in seconds
    
    Returns:
        A secure socket object if connection is successful, None otherwise
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context(cafile=certifi.where())
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        
        # Create a socket and wrap it with SSL
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                print(f"Connected securely to {host}:{port}")
                return secure_sock
                
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        print(f"Connection failed: {e}")
        return None

# Example usage
if __name__ == "__main__":
    HOST = "example.com"  # Replace with actual host
    PORT = 443  # Standard HTTPS port
    
    secure_socket = secure_connect(HOST, PORT)
    if secure_socket:
        # Use the secure socket for further communication
        secure_socket.close()
```