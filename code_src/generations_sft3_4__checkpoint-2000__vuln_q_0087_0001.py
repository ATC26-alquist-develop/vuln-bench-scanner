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
        self.server_url = server_url
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        
    def check_server(self) -> bool:
        """
        Check if the server is available.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            response = requests.get(self.server_url, timeout=10)
            return response.status_code == 200
        except requests.RequestException as e:
            self.logger.error(f"Error checking server: {e}")
            return False

    def monitor(self) -> None:
        """
        Monitor the server continuously.
        """
        while True:
            if self.check_server():
                self.logger.info("Server is available")
            else:
                self.logger.warning("Server is not available")
            
            time.sleep(self.check_interval)

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Get server URL from user input
    server_url = input("Enter server URL to monitor: ").strip()
    
    # Validate server URL
    if not server_url.startswith(('http://', 'https://')):
        logging.error("Invalid URL format. Please enter a valid HTTP or HTTPS URL.")
        return
    
    # Create and start the monitor
    monitor = ServerMonitor(server_url)
    monitor.monitor()

if __name__ == "__main__":
    main()