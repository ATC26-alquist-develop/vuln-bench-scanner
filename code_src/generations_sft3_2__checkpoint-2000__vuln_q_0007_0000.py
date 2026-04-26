```python
import os
import pathlib
import logging
from typing import Optional
import stat
import shutil
from datetime import datetime
import secrets

class SecureFileManager:
    def __init__(self, base_directory: str, max_file_size: int = 100_000_000):
        """Initialize with strict security controls"""
        # Convert to absolute path and validate
        self.base_dir = pathlib.Path(base_directory).resolve()
        if not self.base_dir.is_dir():
            raise ValueError("Base directory must exist and be a directory")
            
        self.max_file_size = max_file_size
        # Setup logging
        logging.basicConfig(
            filename='file_manager.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _validate_path(self, file_path: pathlib.Path) -> bool:
        """Validate file path is within base directory"""
        try:
            path = pathlib.Path(file_path).resolve()
            return path.is_file() and self.base_dir in path.parents
        except (ValueError, RuntimeError):
            return False
            
    def _get_file_hash(self, file_path: pathlib.Path) -> str:
        """Calculate file hash for integrity checks"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except (IOError, OSError):
            return ''
            
    def create_file(self, filename: str, content: str) -> bool:
        """Securely create a new file with proper permissions"""
        try:
            # Sanitize filename
            safe_filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
            file_path = (self.base_dir / safe_filename).with_suffix('.txt')
            
            # Check size
            if len(content.encode('utf-8')) > self.max_file_size:
                logging.warning(f"File size limit exceeded for {safe_filename}")
                return False
                
            # Create file with secure permissions
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
            
            # Log creation
            logging.info(f"File created: {safe_filename}")
            return True
            
        except (IOError, OSError) as e:
            logging.error(f"Error creating file {filename}: {str(e)}")
            return False
            
    def read_file(self, filename: str) -> Optional[str]:
        """Securely read a file with proper access controls"""
        try:
            file_path = (self.base_dir / filename).with_suffix('.txt')
            
            # Validate path
            if not self._validate_path(file_path):
                logging.warning(f"Invalid file path: {filename}")
                return None
                
            # Check file exists and is within base directory
            if not file_path.is_file():
                logging.warning(f"File not found: {filename}")
                return None
                
            # Read file with proper permissions
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Log read
            logging.info(f"File read: {filename}")
            return content
            
        except (IOError, OSError) as e:
            logging.error(f"Error reading file {filename}: {str(e)}")
            return None
            
    def delete_file(self, filename: str) -> bool:
        """Securely delete a file"""
        try:
            file_path = (self.base_dir / filename).with_suffix('.txt')
            
            # Validate path
            if not self._validate_path(file_path):
                logging.warning(f"Invalid file path: {filename}")
                return False
                
            # Check file exists and is within base directory
            if not file_path