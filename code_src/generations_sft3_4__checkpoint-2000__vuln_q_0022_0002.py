import os
import secrets
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
from typing import Optional
import magic
import hashlib

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = Path('/path/to/secure/upload/directory')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_FILENAME_LENGTH = 255

def is_safe_file(filename: str, file_content: bytes) -> bool:
    """Validate file extension and content type."""
    try:
        # Check file extension
        if not allowed_file(filename):
            return False
        
        # Check file content
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file_content)
        if file_type not in ['text/plain', 'application/pdf', 'image/png', 
                            'image/jpeg', 'image/gif']:
            return False
            
        return True
    except Exception:
        return False

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file() -> tuple:
    """Secure file upload endpoint."""
    if 'file' not in request.files:
        abort(400, description="No file part in the request")
        
    file = request.files['file']
    
    if file.filename == '':
        abort(400, description="No file selected")
        
    if not is_safe_file(file.filename, file.read()):
        abort(400, description="Invalid file")
        
    if len(file.read()) > MAX_FILE_SIZE:
        abort(413, description="File too large")
        
    if len(file.filename) > MAX_FILENAME_LENGTH:
        abort(413, description="Filename too long")
        
    # Generate secure random filename
    filename = secrets.token_hex(16)
    extension = os.path.splitext(file.filename)[1]
    secure_name = f"{filename}{extension}"
    
    # Ensure upload directory exists and is secure
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    os.chmod(UPLOAD_FOLDER, 0o750)  # Restrict permissions
    
    file_path = UPLOAD_FOLDER / secure_name
    file.save(file_path)
    
    # Verify file type again after saving
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(str(file_path))
    if file_type not in ['text/plain', 'application/pdf', 'image/png', 
                        'image/jpeg', 'image/gif']:
        os.remove(file_path)
        abort(400, description="Invalid file type after upload")
    
    # Calculate file hash
    file_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            file_hash.update(chunk)
    
    return {
        'message': 'File uploaded successfully',
        'filename': secure_name,
        'file_hash': file_hash.hexdigest()
    }, 200