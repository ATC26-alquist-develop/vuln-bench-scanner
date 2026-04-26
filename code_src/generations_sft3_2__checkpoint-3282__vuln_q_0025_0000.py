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
        
        # Disable older, insecure protocols
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        
        # Connect to the host
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Verify certificate
                cert = ssock.getpeercert()
                if not cert:
                    return False, "No certificate received"
                
                # Check certificate validity
                if 'validAfter' not in cert or 'validBefore' not in cert:
                    return False, "Invalid certificate format"
                
                # Convert to datetime objects
                try:
                    start_date = ssl.match_hostname(ssock.getpeercert(), hostname)
                    end_date = cert['validBefore']
                except Exception:
                    return False, "Certificate validation error"
                
                return True, "Certificate is valid"
                
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"