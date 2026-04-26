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
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Connect to the URL using a timeout
        with socket.create_connection((urlparse(url).netloc, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=urlparse(url).netloc) as ssock:
                # Get certificate
                cert = ssock.getpeercert(binary_form=True)
                
                # Verify certificate
                if cert:
                    # Check basic validity
                    if 'validFrom' in cert and 'validTo' in cert:
                        valid_from = cert['validFrom'].decode('utf-8')
                        valid_to = cert['validTo'].decode('utf-8')
                        if valid_from and valid_to:
                            # Basic validation of dates
                            try:
                                from_date = ssl.cert_to_date(valid_from)
                                to_date = ssl.cert_to_date(valid_to)
                                if from_date and to_date:
                                    return True, f"Certificate valid from {valid_from} to {valid_to}"
                            except Exception:
                                pass
                    return True, "Certificate found but not fully validated"
                else:
                    return False, "No certificate found"
                    
    except (socket.timeout, ssl.SSLError, socket.error) as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

# Example usage
if __name__ == "__main__":
    url = input("Enter URL to check: ")
    is_valid, message = check_ssl_certificate(url)
    print(f"Certificate Valid: {is_valid}")
    print(f"Message: {message}")