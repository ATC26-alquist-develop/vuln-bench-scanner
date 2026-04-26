import ssl
import socket
import re
from typing import Tuple
from urllib.parse import urlparse

def validate_ssl_certificate(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """
    Safely check if a website's SSL certificate is valid.
    
    Args:
        url: The URL to check (must be HTTPS)
        timeout: Connection timeout in seconds
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    # Validate input URL
    if not isinstance(url, str):
        return False, "Invalid URL type"
    
    # Basic URL format validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False, "Invalid URL format"

    try:
        # Parse URL
        parsed_url = urlparse(url)
        if parsed_url.scheme != 'https':
            return False, "URL must use HTTPS protocol"

        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Make connection attempt with timeout
        with socket.create_connection((parsed_url.hostname, parsed_url.port or 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=parsed_url.hostname) as secure_sock:
                # Get certificate
                cert = secure_sock.getpeercert(binary_form=True)
                
                # Verify certificate
                if cert:
                    # Check basic validity
                    if 'validFrom' in cert and 'validTo' in cert:
                        valid_from = cert['validFrom'].decode('ascii')
                        valid_to = cert['validTo'].decode('ascii')
                        # Convert to datetime for comparison
                        from_date = ssl.cert_to_dts(cert['validFrom'])
                        to_date = ssl.cert_to_dts(cert['validTo'])
                        if from_date <= ssl.DTS.now() <= to_date:
                            return True, "Certificate is valid"
                        else:
                            return False, "Certificate expired"
                    else:
                        return False, "Certificate missing valid dates"
                else:
                    return False, "No certificate returned"
                    
    except (socket.gaierror, socket.timeout, ssl.SSLError) as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

# Example usage
if __name__ == "__main__":
    result, message = validate_ssl_certificate("https://example.com")
    print(f"Result: {result}")
    print(f"Message: {message}")