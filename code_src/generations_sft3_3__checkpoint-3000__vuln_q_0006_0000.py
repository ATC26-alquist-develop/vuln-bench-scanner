import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_secure_logger(log_file_path: str, max_size_bytes: int = 10485760, backup_count: int = 5) -> logging.Logger:
    """
    Set up a secure logger that can be read/written to by all users.
    
    Args:
        log_file_path: Path to the log file
        max_size_bytes: Maximum size of each log file before rotation (default 10MB)
        backup_count: Number of backup files to keep (default 5)
        
    Returns:
        Configured logger object
        
    Raises:
        ValueError: If log file path is invalid or directory doesn't exist
    """
    # Validate log file path
    try:
        log_path = Path(log_file_path).resolve()
        if not log_path.parent.exists():
            raise ValueError("Log directory does not exist")
        if not os.access(log_path.parent, os.W_OK):
            raise ValueError("No write permission for log directory")
    except Exception as e:
        raise ValueError(f"Invalid log file path: {str(e)}")

    # Configure logger with rotation to prevent unbounded file growth
    logger = logging.getLogger("secure_logger")
    logger.setLevel(logging.INFO)
    
    # Use RotatingFileHandler to implement log rotation
    handler = RotatingFileHandler(
        filename=str(log_path),
        mode='a',
        maxBytes=max_size_bytes,
        backupCount=backup_count
    )
    
    # Set secure permissions on log file
    os.chmod(log_path, 0o600)  # Read/write for owner only
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger