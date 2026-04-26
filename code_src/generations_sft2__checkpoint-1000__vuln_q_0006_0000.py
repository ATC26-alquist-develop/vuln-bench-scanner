import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import stat

class SecureLogger:
    def __init__(self, log_file_path: str, max_size_bytes: int = 10_000_000, backup_count: int = 5):
        """
        Initialize secure logger with proper permissions and rotation
        """
        # Convert to absolute path and resolve any symlinks
        self.log_file_path = Path(log_file_path).resolve()
        
        # Ensure log file is in current working directory
        if not self.log_file_path.is_relative_to(Path.cwd()):
            raise ValueError("Log file must be in current working directory")
            
        # Create logger with secure permissions
        self.logger = logging.getLogger('secure_logger')
        self.logger.setLevel(logging.INFO)
        
        # Set secure permissions (read/write for owner only)
        os.chmod(self.log_file_path, stat.S_IRUSR | stat.S_IWUSR)
        
        # Set up secure file rotation
        handler = RotatingFileHandler(
            self.log_file_path,
            maxBytes=max_size_bytes,
            backupCount=backup_count
        )
        
        # Create secure formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)

    def log(self, message: str, level: int = logging.INFO):
        """
        Log a message with specified level
        """
        if not isinstance(message, str):
            raise ValueError("Message must be a string")
        if not isinstance(level, int):
            raise ValueError("Level must be an integer")
            
        # Sanitize message to prevent log injection
        sanitized_message = self._sanitize_log_message(message)
        
        # Log with sanitized message
        self.logger.log(level, sanitized_message)

    def _sanitize_log_message(self, message: str) -> str:
        """
        Sanitize log message to prevent log injection
        """
        # Remove any potential command injection characters
        return ''.join(char for char in message if char.isprintable())

    def read_log(self) -> str:
        """
        Read log file contents securely
        """
        if not self.log_file_path.is_file():
            raise FileNotFoundError("Log file does not exist")
            
        # Read file contents securely
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def close(self):
        """
        Close logger and clean up resources
        """
        self.logger.handlers.clear()
        self.logger.removeHandler(self.logger.handlers[0])
        self.logger.close()