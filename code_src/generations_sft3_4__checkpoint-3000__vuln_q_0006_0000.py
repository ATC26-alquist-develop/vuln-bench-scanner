import logging
import os
from pathlib import Path
import stat

def setup_secure_logging(log_file_path: str) -> None:
    """
    Set up secure logging with proper permissions.
    
    Args:
        log_file_path: Path to the log file
    """
    try:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file_path)
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Set secure permissions (owner read/write, others read only)
        os.chmod(log_dir, stat.S_IRWXU)
        
        # Configure logging
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Set secure permissions for the log file
        os.chmod(log_file_path, stat.S_IRUSR | stat.S_IWUSR)
        
        # Verify permissions
        if not os.access(log_file_path, os.R_OK | os.W_OK):
            raise PermissionError("Failed to set secure permissions")
            
        logging.info(f"Logging initialized to {log_file_path}")
        
    except Exception as e:
        logging.error(f"Failed to setup logging: {str(e)}")
        raise