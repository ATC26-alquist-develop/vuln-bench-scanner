import socket
import ssl
import logging
from typing import Optional

def create_secure_connection(host: str, port: int) -> Optional[ssl.SSLSocket]:
    """
    Creates a secure SSL socket connection to the specified host and port.
    
    Args:
        host (str): The hostname or IP address to connect to
        port (int): The port number to connect to
        
    Returns:
        Optional[ssl.SSLSocket]: The created SSL socket or None if connection fails
        
    Raises:
        ssl.SSLError: If SSL/TLS handshake fails
        socket.error: If socket connection fails
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        
        # Set secure options
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        
        # Create a socket and wrap it with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=host)
        
        # Connect to the server
        secure_sock.connect((host, port))
        
        return secure_sock
        
    except (ssl.SSLError, socket.error) as e:
        logging.error(f"Failed to create secure connection: {str(e)}")
        return None

def close_connection(ssl_socket: ssl.SSLSocket) -> None:
    """
    Closes the SSL socket connection properly.
    
    Args:
        ssl_socket (ssl.SSLSocket): The SSL socket to close
        
    Raises:
        ssl.SSLError: If SSL shutdown fails
    """
    try:
        ssl_socket.shutdown(socket.SHUT_RDWR)
        ssl_socket.close()
    except ssl.SSLError as e:
        logging.error(f"Failed to close SSL connection: {str(e)}")
        raise

def main():
    host = "example.com"
    port = 443
    
    try:
        # Create and use the secure connection
        ssl_socket = create_secure_connection(host, port)
        if ssl_socket:
            # Perform operations with the secure connection
            ssl_socket.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            response = ssl_socket.recv(4096)
            print(f"Received response: {response}")
            
            # Close the connection
            close_connection(ssl_socket)
            
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        # Ensure the connection is always closed
        if ssl_socket:
            close_connection(ssl_socket)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()