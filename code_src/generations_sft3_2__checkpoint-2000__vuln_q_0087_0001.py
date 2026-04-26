import requests
import time
import logging
from typing import Optional

class ServerMonitor:
    def __init__(self, server_url: str, check_interval: int = 300):
        """
        Initialize the server monitor with the server URL and check interval.
        
        Args:
            server_url (str): The URL of the server to monitor
            check_interval (int): Time between checks in seconds
        """
        if not isinstance(server_url, str) or not server_url:
            raise ValueError("Server URL must be a non-empty string")
        if not isinstance(check_interval, int) or check_interval <= 0:
            raise ValueError("Check interval must be a positive integer")
            
        self.server_url = server_url
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)
        
    def check_server(self) -> bool:
        """
        Check the availability of the server using HTTPS.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            # Use HTTPS for secure communication
            response = requests.get(
                self.server_url,
                timeout=10,
                verify=True  # Verify SSL certificates
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking server: {str(e)}")
            return False

    def monitor(self) -> Optional[str]:
        """
        Monitor the server and return status message.
        
        Returns:
            Optional[str]: Status message or None if server is unavailable
        """
        while True:
            if self.check_server():
                self.logger.info("Server is available")
                return "Server is available"
            else:
                self.logger.warning("Server is not available")
                time.sleep(self.check_interval)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    monitor = ServerMonitor("https://example.com")
    monitor.monitor()