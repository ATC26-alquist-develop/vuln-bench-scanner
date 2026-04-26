import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
import stat

def setup_secure_logging(log_file_path: str, max_size_bytes: int = 10485760, backup_count: int = 5) -> logging.Logger:
    """
    Sets up secure logging with proper access controls.
    
    Args:
        log_file_path: Path to the log file
        max_size_bytes: Maximum size of each log file before rotation
        backup_count: Number of backup files to keep
    
    Returns:
        Configured logging.Logger object
    """
    # Convert to absolute path and validate
    log_path = Path(log_file_path).resolve()
    
    # Ensure directory exists and has proper permissions
    log_dir = log_path.parent
    if not log_dir.exists():
        log_dir.mkdir(mode=0o755, parents=True)
    
    # Set secure permissions (owner read/write only)
    os.chmod(log_dir, stat.S_IRWXU)
    
    # Configure logging
    logger = logging.getLogger('secure_app')
    logger.setLevel(logging.INFO)
    
    # Create rotating file handler with secure permissions
    file_handler = RotatingFileHandler(
        filename=str(log_path),
        mode='a',
        maxBytes=max_size_bytes,
        backupCount=backup_count
    )
    
    # Set secure permissions on log file
    os.chmod(log_path, stat.S_IRUSR | stat.S_IWUSR)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    
    return logger