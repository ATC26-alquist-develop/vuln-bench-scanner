```python
import socket
import ssl
from typing import Optional

def create_secure_connection(host: str, port: int, timeout: int = 10) -> Optional[socket.socket]:
    """
    Create a secure SSL/TLS connection to the specified host and port.
    
    Args:
        host: The hostname or IP address to connect to
        port: The port number to connect to
        timeout: Connection timeout in seconds
    
    Returns:
        A secure socket object if connection is successful, None otherwise
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        
        # Create a socket and wrap it with SSL
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                return secure_sock
    except (socket.error, ssl.SSLError, OSError) as e:
        print(f"Connection failed: {e}")
        return None

def main():
    host = "example.com"  # Replace with actual host
    port = 443  # Standard HTTPS port
    
    secure_socket = create_secure_connection(host, port)
    if secure_socket:
        print("Secure connection established")
        secure_socket.close()
        print("Connection closed")
    else:
        print("Failed to establish secure connection")

if __name__ == "__main__":
    main()
```