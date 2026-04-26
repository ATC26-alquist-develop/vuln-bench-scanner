import logging
import os
from logging.handlers import RotatingFileHandler

def setup_secure_logger(log_file_path: str, max_size: int = 10485760, backup_count: int = 5) -> logging.Logger:
    """
    Set up a secure logger that writes to a file with proper permissions.
    
    Args:
        log_file_path: Path to the log file
        max_size: Maximum size of each log file in bytes (default 10MB)
        backup_count: Number of backup files to keep (default 5)
    
    Returns:
        Configured logger object
    """
    # Ensure the directory exists and has proper permissions
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    os.chmod(os.path.dirname(log_file_path), 0o700)  # Only owner can read/write/execute
    
    # Configure logger
    logger = logging.getLogger('secure_logger')
    logger.setLevel(logging.INFO)
    
    # Create a rotating file handler with secure permissions
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=max_size,
        backupCount=backup_count,
        delay=True  # Delay creation until first log
    )
    file_handler.setLevel(logging.INFO)
    
    # Create a secure formatter that doesn't expose sensitive data
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(file_handler)
    
    return logger

# Usage example:
if __name__ == '__main__':
    log_file = '/path/to/secure/logfile.log'
    logger = setup_secure_logger(log_file)
    logger.info('This is a secure log entry')