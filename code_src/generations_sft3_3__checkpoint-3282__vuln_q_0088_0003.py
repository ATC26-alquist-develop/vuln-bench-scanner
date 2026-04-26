import os
import ftplib
from typing import Optional
import logging
from pathlib import Path

class SecureFTPClient:
    def __init__(self, host: str, port: int = 21):
        """Initialize secure FTP client with proper error handling."""
        if not isinstance(host, str) or not host:
            raise ValueError("Invalid host parameter")
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError("Invalid port number")
            
        self.host = host
        self.port = port
        self._connection: Optional[ftplib.FTP] = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SecureFTPClient')

    def connect(self, username: str, password: str) -> bool:
        """Establish secure connection to FTP server."""
        try:
            # Validate inputs
            if not all(isinstance(x, str) and x for x in [username, password]):
                raise ValueError("Invalid credentials format")
                
            # Create connection with timeout and TLS
            self._connection = ftplib.FTP_TLS(
                host=self.host,
                port=self.port,
                timeout=30
            )
            
            # Force TLS
            self._connection.prot_p()
            
            # Attempt login
            result = self._connection.login(username, password)
            
            if not result.startswith('230'):
                self.logger.error("Login failed")
                return False
                
            self.logger.info("Successfully connected to FTP server")
            return True
            
        except (ftplib.all_errors, ValueError, OSError) as e:
            self.logger.error(f"Connection error: {str(e)}")
            self._connection = None
            return False

    def disconnect(self) -> None:
        """Safely disconnect from FTP server."""
        try:
            if self._connection:
                self._connection.quit()
                self._connection = None
        except Exception as e:
            self.logger.error(f"Error during disconnection: {str(e)}")

    def __enter__(self):
        """Context manager entry for proper resource handling."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure proper cleanup on exit."""
        self.disconnect()

# Example usage
if __name__ == "__main__":
    try:
        with SecureFTPClient("ftp.example.com", 21) as client:
            if client.connect("username", "password"):
                # Perform operations here
                pass
    except Exception as e:
        logging.error(f"Operation failed: {str(e)}")