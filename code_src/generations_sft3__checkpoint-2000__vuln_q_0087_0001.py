import requests
import logging
from typing import Optional
from urllib.parse import urlparse
import ssl

class SecureServerMonitor:
    def __init__(self, server_url: str, timeout: int = 5, max_retries: int = 3):
        """
        Initialize the server monitor with security controls
        
        Args:
            server_url: The URL of the server to monitor
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        # Validate URL
        parsed_url = urlparse(server_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid server URL")
        
        self.server_url = server_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # Configure secure SSL context
        self.session.verify = True  # Enforce SSL certificate verification
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def check_server_availability(self) -> bool:
        """
        Check if the server is available
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            for attempt in range(self.max_retries):
                response = self.session.get(
                    self.server_url,
                    timeout=self.timeout,
                    allow_redirects=False  # Prevent redirect attacks
                )
                response.raise_for_status()
                return True
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Server check failed: {str(e)}")
            return False

    def close(self):
        """
        Close the session and release resources
        """
        self.session.close()

def main():
    # Example usage
    monitor = SecureServerMonitor("https://example.com")
    if monitor.check_server_availability():
        print("Server is available")
    else:
        print("Server is not available")
    monitor.close()

if __name__ == "__main__":
    main()