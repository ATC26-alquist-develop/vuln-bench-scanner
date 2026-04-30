```python
import os
import hashlib
from typing import Optional
from pathlib import Path
import magic
from werkzeug.utils import secure_filename
import hashlib

class SecureFileHandler:
    def __init__(self, upload_dir: str, max_file_size: int = 10_000_000):
        """
        Initialize secure file handler with upload directory and max file size.
        
        Args:
            upload_dir: Absolute path to the upload directory
            max_file_size: Maximum allowed file size in bytes (default 10MB)
        """
        self.upload_dir = Path(upload_dir).resolve()
        self.max_file_size = max_file_size
        # Ensure upload directory exists and is secure
        if not self.upload_dir.exists():
            self.upload_dir.mkdir(mode=0o750, parents=True, exist_ok=True)

    def validate_file(self, file) -> Optional[str]:
        """
        Validate uploaded file for security.
        
        Args:
            file: File object from request
            
        Returns:
            Secure filename if valid, None otherwise
        """
        # Check if file is actually present
        if not file:
            return None
            
        # Validate file size
        file.seek(0, os.SEEK_END)
        if file.tell() > self.max_file_size:
            return None
        file.seek(0)  # Reset file pointer
        
        # Validate file type using magic numbers
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file.read(1024))
        file.seek(0)  # Reset file pointer
        
        # Whitelist of allowed MIME types
        allowed_types = {'image/jpeg', 'image/png', 'application/pdf'}
        if file_type not in allowed_types:
            return None
            
        # Generate secure filename
        filename = secure_filename(file.filename)
        
        # Validate filename extension
        if not filename.lower().split('.')[-1] in allowed_types:
            return None
            
        # Check if file already exists
        if (self.upload_dir / filename).exists():
            return None
            
        return filename

    def save_file(self, file, filename: str) -> Path:
        """
        Save validated file securely.
        
        Args:
            file: File object from request
            filename: Original filename
            
        Returns:
            Path to saved file
        """
        try:
            # Generate unique filename to prevent overwriting
            file_extension = Path(filename).suffix
            unique_filename = f"{hashlib.sha256(filename.encode()).hexdigest()}{file_extension}"
            
            # Create full path and validate it's within upload directory
            file_path = (self.upload_dir / unique_filename).resolve()
            if self.upload_dir not in file_path.parents:
                raise ValueError("Invalid file path")
            
            # Save file with secure permissions
            with open(file_path, 'wb') as f:
                f.write(file.read())
            
            # Set secure permissions (read-only for owner)
            os.chmod(file_path.stat().st_mode & ~0o222, stat.S_IRUSR)
            
            return file_path
        except Exception as e:
            # Log error here if needed
            raise ValueError(f"Error saving file: {str(e)}")

# Example usage with Flask
from flask import Flask, request, jsonify
app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/secure/upload/directory'
file_handler = SecureFileHandler(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        filename = file_handler.validate_file(file)
        if not filename:
            return jsonify({"error": "Invalid file"}