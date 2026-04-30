```python
import os
import sys
import hashlib
from pathlib import Path
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_file_path(file_path: str) -> Optional[str]:
    """
    Validate the provided file path.
    
    Args:
        file_path: The file path to validate
        
    Returns:
        Validated file path or None if invalid
    """
    try:
        # Convert to absolute path and resolve any symlinks
        path = Path(file_path).resolve()
        
        # Check if file exists and is a regular file
        if not path.is_file():
            logging.error(f"File does not exist or is not a regular file: {path}")
            return None
            
        # Check if we have read permissions
        if not path.is_readable():
            logging.error(f"No read permission for file: {path}")
            return None
            
        return str(path)
    except Exception as e:
        logging.error(f"Error validating file path: {str(e)}")
        return None

def calculate_file_hash(file_path: str) -> str:
    """
    Calculate SHA-256 hash of file.
    
    Args:
        file_path: The file path to calculate hash for
        
    Returns:
        SHA-256 hash of the file
    """
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating file hash: {str(e)}")
        return ""

def download_file(file_path: str) -> None:
    """
    Download file to current directory.
    
    Args:
        file_path: The file path to download
    """
    try:
        # Validate file path
        validated_path = validate_file_path(file_path)
        if not validated_path:
            return
            
        # Calculate file hash
        file_hash = calculate_file_hash(validated_path)
        if not file_hash:
            return
            
        # Create a new filename with hash
        new_filename = f"{Path(validated_path).stem}_{file_hash}{Path(validated_path).suffix}"
        new_path = Path(validated_path).parent / new_filename
        
        # Download file
        try:
            with open(validated_path, 'rb') as source, open(new_path, 'wb') as target:
                target.write(source.read())
            logging.info(f"File downloaded successfully: {new_path}")
        except Exception as e:
            logging.error(f"Error downloading file: {str(e)}")

def main() -> None:
    """
    Main function to handle command-line arguments and initiate download.
    """
    if len(sys.argv) != 2:
        logging.error("Usage: python script.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    download_file(file_path)

if __name__ == "__main__":
    main()
```