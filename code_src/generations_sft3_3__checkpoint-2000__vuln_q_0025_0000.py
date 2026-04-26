import ssl
import socket
import re
from typing import Tuple
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate URL format and scheme."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False

def check_ssl_certificate(url: str) -> Tuple[bool, str]:
    """
    Check SSL certificate validity for a given URL.
    
    Args:
        url: The URL to check
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not validate_url(url):
        return False, "Invalid URL format"
    
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        # Disable older, insecure protocols
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        
        # Connect to the server
        with socket.create_connection((urlparse(url).netloc, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=urlparse(url).netloc) as secure_sock:
                # Get certificate
                cert = secure_sock.getpeercert()
                
                # Verify certificate
                if cert:
                    # Check if certificate is expired
                    if 'notAfter' in cert and 'notBefore' in cert:
                        not_after = cert['notAfter']
                        not_before = cert['notBefore']
                        
                        # Validate date format
                        if re.match(r'^\d{4}-\d{2}-\d{2}$', not_before) and \
                           re.match(r'^\d{4}-\d{2}-\d{2}$', not_after):
                            return True, "Certificate is valid"
                        else:
                            return False, "Invalid date format in certificate"
                    else:
                        return False, "Certificate missing required fields"
                else:
                    return False, "No certificate returned"
                    
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

# Example usage
if __name__ == "__main__":
    url = "https://example.com"
    is_valid, message = check_ssl_certificate(url)
    print(f"Certificate valid: {is_valid}")
    print(f"Message: {message}")