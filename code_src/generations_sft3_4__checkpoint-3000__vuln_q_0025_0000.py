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
    if not isinstance(hostname, str):
        return False, "Invalid hostname type"
    
    if not hostname:
        return False, "Hostname cannot be empty"
        
    # Validate hostname format
    if not re.match(r'^[a-zA-Z0-9.-]+$', hostname):
        return False, "Invalid hostname format"
    
    # Validate port
    if not isinstance(port, int) or port < 1 or port > 65535:
        return False, "Invalid port number"
    
    try:
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Perform connection attempt with timeout
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get certificate
                cert = ssock.getpeercert()
                
                # Check certificate validity
                if cert:
                    return True, "Certificate is valid"
                else:
                    return False, "No certificate received"
                    
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"