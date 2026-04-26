import ssl
import socket
import re
from typing import Tuple
from urllib.parse import urlparse

def validate_ssl_cert(hostname: str, port: int = 443) -> Tuple[bool, str]:
    """
    Securely check SSL certificate validity for a given hostname.
    
    Args:
        hostname: Target hostname to validate
        port: Target port (default 443)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Input validation
    if not isinstance(hostname, str) or not isinstance(port, int):
        return False, "Invalid input types"
    
    if port < 1 or port > 65535:
        return False, "Invalid port number"
    
    # Validate hostname format
    if not re.match(r'^[a-zA-Z0-9.-]+$', hostname):
        return False, "Invalid hostname format"
    
    try:
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Disable older, insecure protocols
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        
        # Connect to verify certificate
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get certificate
                cert = ssock.getpeercert()
                
                # Verify certificate
                if cert:
                    return True, "Certificate valid"
                else:
                    return False, "No certificate received"
                    
    except ssl.SSLError as e:
        return False, f"SSL error: {str(e)}"
    except socket.error as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
    
    return False, "Operation completed"

# Example usage
if __name__ == "__main__":
    result, message = validate_ssl_cert("example.com")
    print(f"Result: {result}")
    print(f"Message: {message}")