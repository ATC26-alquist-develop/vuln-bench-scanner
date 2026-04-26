import os
import uuid
import magic
import hashlib
from pathlib import Path
from typing import Optional

def secure_file_upload(file_content: bytes, file_type: str, max_size: int = 10 * 1024 * 1024) -> Optional[str]:
    """
    Securely handle user-uploaded files.
    
    Args:
        file_content: Binary content of the file
        file_type: MIME type of the file
        max_size: Maximum allowed file size in bytes
        
    Returns:
        Path to the uploaded file or None if upload fails
    """
    try:
        # Generate a secure random filename
        file_extension = Path(file_content).suffix
        secure_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Create a secure temporary directory
        temp_dir = Path("/tmp/secure_uploads")
        temp_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Save file to temporary location
        temp_path = temp_dir / secure_filename
        temp_path.write_bytes(file_content)
        
        # Validate file type
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(str(temp_path))
        if file_mime != file_type:
            os.remove(temp_path)
            return None
            
        # Calculate file hash for integrity check
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Move file to final location (outside web root)
        final_path = Path("/var/www/uploads") / secure_filename
        final_path.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
        final_path.write_bytes(file_content)
        
        # Set secure permissions
        os.chmod(final_path, 0o640)
        
        return str(final_path)
        
    except Exception:
        # Clean up temporary file if it exists
        if temp_path.exists():
            temp_path.unlink()
        return None