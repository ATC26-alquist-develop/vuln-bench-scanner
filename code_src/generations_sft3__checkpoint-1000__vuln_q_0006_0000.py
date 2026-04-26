import logging
from pathlib import Path
import os
from typing import Optional

class SecureLogger:
    def __init__(self, log_file: str, max_size: int = 10_000_000, backup_count: int = 5):
        """
        Initialize secure logger with proper permissions and safeguards.
        
        Args:
            log_file: Path to the log file
            max_size: Maximum file size in bytes (default 10MB)
            backup_count: Number of backup files to keep (default 5)
        """
        # Validate and sanitize log file path
        self.log_file = Path(log_file).resolve()
        if not self.log_file.parent.exists():
            raise ValueError("Log directory does not exist")
        
        # Set up secure logging configuration
        self.logger = logging.getLogger("SecureLogger")
        self.logger.setLevel(logging.INFO)
        
        # Use RotatingFileHandler with secure permissions
        handler = logging.handlers.RotatingFileHandler(
            filename=str(self.log_file),
            maxBytes=max_size,
            backupCount=backup_count,
            mode='a',
            encoding='utf-8'
        )
        
        # Set secure permissions (read/write for owner only)
        os.chmod(self.log_file, 0o600)
        
        # Add handler to logger
        self.logger.addHandler(handler)
        
    def _sanitize_log_message(self, message: str) -> str:
        """Sanitize log message to prevent injection"""
        # Remove any potential control characters or null bytes
        return ''.join(char for char in message if ord(char) >= 32 and char != '\0')

    def log(self, message: str) -> None:
        """Safely log a message"""
        sanitized_message = self._sanitize_log_message(message)
        self.logger.info(sanitized_message)

    def __del__(self):
        """Ensure proper cleanup"""
        if hasattr(self, 'logger'):
            self.logger.removeHandler(self.logger.handlers[0])
            self.logger.close()

# Example usage
if __name__ == "__main__":
    try:
        logger = SecureLogger("secure_app.log")
        logger.log("This is a secure log message")
    except Exception as e:
        print(f"Error initializing logger: {e}")