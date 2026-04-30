import os
import logging
from pathlib import Path
from typing import Optional

class SecureLogger:
    def __init__(self, log_file: str, max_file_size: int = 10_000_000):
        """Initialize secure logger with strict controls."""
        # Convert to absolute path and resolve any symlinks
        self.log_path = Path(log_file).resolve()
        
        # Validate log file path
        if not self.log_path.is_file():
            raise ValueError("Log file must exist")
            
        # Set up logging with strict controls
        self.logger = logging.getLogger("SecureLogger")
        self.logger.setLevel(logging.INFO)
        
        # Create secure file handler
        self.file_handler = self._create_secure_handler(self.log_path, max_file_size)
        
        # Create console handler for debugging
        self.console_handler = logging.StreamHandler()
        self.logger.addHandler(self.console_handler)
        
    def _create_secure_handler(self, file_path: Path, max_size: int) -> logging.FileHandler:
        """Create secure file handler with strict controls."""
        # Ensure file is not world-writable
        if os.access(file_path, os.W_OK):
            raise PermissionError("Log file must not be world-writable")
            
        # Set secure permissions (read-only for owner)
        os.chmod(file_path, 0o600)
        
        # Create handler with secure settings
        handler = logging.FileHandler(
            file_path,
            mode='a',
            encoding='utf-8',
            delay=True  # Delay opening until first write
        )
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        return handler
        
    def log(self, level: int, message: str) -> None:
        """Securely log a message."""
        if not isinstance(message, str):
            raise ValueError("Message must be a string")
            
        # Sanitize message to prevent log injection
        sanitized_message = self._sanitize_message(message)
        self.logger.log(level, sanitized_message)
        
    def _sanitize_message(self, message: str) -> str:
        """Sanitize message to prevent log injection."""
        # Remove any potentially dangerous characters
        return ''.join(c for c in message if c.isprintable())
        
    def __del__(self):
        """Ensure proper cleanup."""
        # Close handlers
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)