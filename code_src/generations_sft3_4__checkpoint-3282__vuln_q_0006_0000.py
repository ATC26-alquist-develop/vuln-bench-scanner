import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_secure_logger(log_file_path: str, max_size_bytes: int = 10485760, backup_count: int = 5) -> logging.Logger:
    """
    Set up a secure logger that can be read/written to by all users.
    
    Args:
        log_file_path: Path to the log file
        max_size_bytes: Maximum size of log file before rotation (default 10MB)
        backup_count: Number of backup files to keep (default 5)
        
    Returns:
        Configured logger object
        
    Raises:
        ValueError: If log file path is invalid or directory doesn't exist
    """
    # Validate log file path
    log_path = Path(log_file_path)
    if not log_path.parent.exists():
        raise ValueError("Log directory does not exist")
    
    # Create logger
    logger = logging.getLogger("secure_logger")
    logger.setLevel(logging.INFO)
    
    # Create rotating file handler with secure permissions
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=max_size_bytes,
        backupCount=backup_count
    )
    
    # Set secure permissions (only owner can read/write)
    os.chmod(log_path, 0o600)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    
    return logger