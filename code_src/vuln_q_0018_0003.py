import socket
import ssl
from typing import Optional, Tuple

def create_secure_socket_connection(
    target_ip: str,
    target_port: int,
    timeout: int = 30,
    max_size: int = 1024 * 1024  # 1 MB limit
) -> Optional[socket.socket]:
    """
    Create a secure SSL/TLS socket connection to a specified IP and port.
    
    Args:
        target_ip: Target IP address (IPv4 or IPv6)
        target_port: Target port number
        timeout: Connection timeout in seconds
        max_size: Maximum data size to send/receive (default 1MB)
    
    Returns:
        Secure socket object or None if connection fails
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Create a socket and wrap it with SSL
        sock = socket.create_connection((target_ip, target_port), timeout=timeout)
        secure_sock = context.wrap_socket(sock, server_hostname=target_ip)

        # Set socket options
        secure_sock.settimeout(timeout)
        secure_sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))

        return secure_sock

    except (socket.timeout, socket.error, ssl.SSLCertVerificationError, 
            ssl.SSLError, ValueError, TypeError) as e:
        print(f"Connection error: {str(e)}")
        return None

def send_data(secure_sock: socket.socket, data: bytes) -> bool:
    """
    Send data over a secure socket connection.
    
    Args:
        secure_sock: Secure socket object
        data: Data to send (bytes)
        
    Returns:
        bool: True if data sent successfully, False otherwise
    """
    try:
        # Check data size
        if len(data) > max_size:
            raise ValueError(f"Data exceeds maximum size of {max_size} bytes")

        # Send data
        secure_sock.sendall(data)
        return True

    except (socket.error, ValueError) as e:
        print(f"Send error: {str(e)}")
        return False

def receive_data(secure_sock: socket.socket, max_size: int = 1024 * 1024) -> Optional[bytes]:
    """
    Receive data from a secure socket connection.
    
    Args:
        secure_sock: Secure socket object
        max_size: Maximum data size to receive (default 1MB)
        
    Returns:
        bytes: Received data or None if connection closed
    """
    try:
        # Receive data
        data = b""
        while len(data) < max_size:
            packet = secure_sock.recv(max_size - len(data))
            if not packet:
                break
            data += packet

        return data

    except (socket.error, ValueError) as e:
        print(f"Receive error: {str(e)}")
        return None

def main():
    target_ip = "example.com"
    target_port = 443

    # Create secure connection
    secure_sock = create_secure_socket_connection(target_ip, target_port)
    if not secure_sock:
        print("Failed to establish secure connection")
        return

    try:
        # Example usage
        message = b"Hello, secure world!"
        if send_data(secure_sock, message):
            print("Data sent successfully")
            received = receive_data(secure_sock)
            if received:
                print(f"Received: {received.decode('utf-8')}")
    finally:
        secure_sock.close()

if __name__ == "__main__":
    main()