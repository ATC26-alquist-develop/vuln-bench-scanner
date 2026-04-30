import os
from pathlib import Path
import hashlib
import secrets
from typing import Optional

def secure_download_file(file_path: str, max_size: int = 10 * 1024 * 1024) -> Optional[bytes]:
    """
    Securely download a file from the server.
    
    Args:
        file_path: Path to the file on the server
        max_size: Maximum allowed file size in bytes (default 10MB)
    
    Returns:
        File content as bytes if successful, None if error occurs
    """
    try:
        # Convert to Path object for secure path handling
        file_path = Path(file_path).resolve()
        
        # Validate file path is within allowed directory
        allowed_dir = Path('/path/to/allowed/directory').resolve()
        if not file_path.is_relative_to(allowed_dir):
            raise ValueError("Access denied: File is outside allowed directory")
            
        # Check file size
        if file_path.stat().st_size > max_size:
            raise ValueError(f"File too large: {file_path.stat().st_size} bytes")
            
        # Generate secure random token for download
        download_token = secrets.token_hex(16)
        
        # Open file in binary read mode
        with open(file_path, 'rb') as file:
            content = file.read()
            
        # Calculate file hash
        file_hash = hashlib.sha256(content).hexdigest()
        
        return {
            'content': content,
            'token': download_token,
            'hash': file_hash
        }
        
    except (OSError, ValueError) as e:
        # Log error here if needed
        return None