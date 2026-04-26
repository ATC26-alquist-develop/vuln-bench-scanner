import socket
import ssl
import logging
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_connection(host: str, port: int, timeout: int = 10) -> Tuple[bool, str]:
    """
    Establish a secure SSL/TLS connection to a server.
    
    Args:
        host: Server hostname
        port: Server port
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Create a secure socket
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                logger.info(f"Successfully connected to {host}:{port}")
                return True, "Connection established"
                
    except (socket.timeout, ssl.SSLCertVerificationError) as e:
        logger.error(f"Connection failed to {host}:{port}: {str(e)}")
        return False, f"Connection failed: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error connecting to {host}:{port}: {str(e)}")
        return False, "Unexpected error"

def connect_to_servers(servers: List[Tuple[str, int]]) -> List[Tuple[bool, str]]:
    """
    Establish connections to multiple servers concurrently.
    
    Args:
        servers: List of (host, port) tuples
        
    Returns:
        List of (success: bool, message: str) tuples
    """
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_server = {executor.submit(create_secure_connection, host, port): (host, port) 
                            for host, port in servers}
        for future in as_completed(future_to_server):
            host, port = future_to_server[future]
            try:
                success, message = future.result()
                results.append((success, message))
            except Exception as e:
                logger.error(f"Error processing {host}:{port}: {str(e)}")
                results.append((False, f"Error processing {host}:{port}: {str(e)}"))
                
    return results

if __name__ == "__main__":
    # Example usage
    servers = [
        ("example.com", 443),
        ("api.example.com", 443),
        ("nonexistent.example.com", 443)
    ]
    
    results = connect_to_servers(servers)
    for success, message in results:
        print(f"Server: {message}")