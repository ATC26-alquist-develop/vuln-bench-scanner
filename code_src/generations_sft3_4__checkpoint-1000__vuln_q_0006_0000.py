import logging
from pathlib import Path
import os

def setup_secure_logging(log_file_path: str, max_size: int = 10_000_000, backup_count: int = 5):
    """
    Set up secure logging with proper permissions and rotation.
    
    Args:
        log_file_path: Path to the log file
        max_size: Maximum size of each log file in bytes
        backup_count: Number of backup files to keep
    """
    try:
        # Convert to Path object for secure path handling
        log_path = Path(log_file_path)
        
        # Ensure log directory exists with proper permissions
        log_path.parent.mkdir(parents=True, exist_ok=True)
        os.chmod(log_path.parent, 0o700)  # Restrict permissions to owner only
        
        # Configure logging
        logging.basicConfig(
            filename=str(log_path),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set up rotation
        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(log_path),
            maxBytes=max_size,
            backupCount=backup_count
        )
        
        # Set secure permissions for log file
        os.chmod(log_path, 0o600)
        
        return logging.getLogger(__name__)
    
    except Exception as e:
        logging.error(f"Failed to setup secure logging: {str(e)}")
        return None