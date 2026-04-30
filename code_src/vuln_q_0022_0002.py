```python
import os
from pathlib import Path
from typing import Optional
import hashlib
import magic
from werkzeug.utils import secure_filename
import hashlib
import magic
import secrets

class SecureFileUploader:
    def __init__(self, upload_dir: str, max_file_size: int = 10_000_000):
        """
        Initialize secure file uploader with validation parameters
        
        Args:
            upload_dir: Base directory for file uploads
            max_file_size: Maximum file size in bytes (default 10MB)
        """
        self.upload_dir = Path(upload_dir).resolve()
        self.max_file_size = max_file_size
        self.allowed_extensions = {'.txt', '.pdf', '.png', '.jpg', '.jpeg'}
        
        # Ensure upload directory exists and has proper permissions
        if not self.upload_dir.exists():
            self.upload_dir.mkdir(mode=0o750, parents=True, exist_ok=True)

    def _validate_file(self, file) -> Optional[str]:
        """
        Validate file before processing
        
        Args:
            file: File object from request
            
        Returns:
            Filename if valid, None otherwise
        """
        # Check if file exists and is a valid file
        if not file or not file.filename:
            return None
            
        # Generate secure filename
        filename = secure_filename(file.filename)
        
        # Validate file extension
        if not filename.lower().endswith(tuple(self.allowed_extensions)):
            return None
            
        # Validate file size
        file.seek(0, os.SEEK_END)
        if file.tell() > self.max_file_size:
            return None
        file.seek(0)  # Reset file pointer
        
        # Validate file type using libmagic
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file.read(2048))
        file.seek(0)  # Reset file pointer
        
        if not file_type.startswith('application/'):
            return None
            
        return filename

    def upload_file(self, file) -> str:
        """
        Securely upload file to server
        
        Args:
            file: File object from request
            
        Returns:
            Path to uploaded file or None if upload failed
        """
        try:
            # Validate file
            filename = self._validate_file(file)
            if not filename:
                return None

            # Generate unique filename to prevent overwriting
            file_hash = secrets.token_hex(8)
            extension = filename.split('.')[-1]
            new_filename = f"{file_hash}.{extension}"

            # Create full file path
            file_path = self.upload_dir / new_filename

            # Securely save file
            with open(file_path, 'wb') as f:
                file.save(f, mimetype='application/octet-stream')

            # Verify file type after saving
            if not self._validate_file(file):
                os.remove(file_path)
                return None

            return str(file_path)

        except Exception as e:
            # Log error here
            return None
```