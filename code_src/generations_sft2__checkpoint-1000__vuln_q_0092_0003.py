import os
import hashlib
from pathlib import Path
from typing import Optional
import secrets

def generate_secure_filename(original_filename: str) -> str:
    """Generate a secure random filename to prevent path traversal attacks."""
    return secrets.token_hex(16)

def download_file(file_path: str, user_id: str) -> Optional[str]:
    """
    Securely download a file from the server.
    
    Args:
        file_path: Path to the file on the server
        user_id: User identifier (e.g., username or user ID)
    
    Returns:
        Downloaded file content as a string, or None if download fails
    """
    try:
        # Convert to absolute path and resolve any symlinks
        file_path = os.path.abspath(os.path.realpath(file_path))
        
        # Ensure the file exists and is within the allowed directory
        allowed_dir = '/path/to/allowed/directory'  # Set this to your actual allowed directory
        if not file_path.startswith(allowed_dir):
            raise ValueError("Access denied: File is outside allowed directory")
            
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found")
            
        # Generate a secure random filename
        secure_filename = generate_secure_filename(os.path.basename(file_path))
        secure_file_path = os.path.join('/path/to/download/directory', secure_filename)
        
        # Open the file in binary mode and read its contents
        with open(file_path, 'rb') as source_file, open(secure_file_path, 'wb') as dest_file:
            while True:
                chunk = source_file.read(8192)  # Read in 8KB chunks
                if not chunk:
                    break
                dest_file.write(chunk)
                
        # Generate and return the file's SHA-256 hash
        with open(secure_file_path, 'rb') as file:
            file_hash = hashlib.sha256(file.read()).hexdigest()
            
        return f"File content (SHA-256: {file_hash})"
        
    except Exception as e:
        # Log the error securely (implement secure logging mechanism)
        print(f"Error downloading file: {str(e)}")
        return None