import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
import magic
import hashlib
from typing import Optional

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = Path('/path/to/secure/upload/directory')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit
MAX_FILENAME_LENGTH = 255

def is_safe_file(filename: str, file_content: bytes) -> bool:
    """Validate file extension and content type."""
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
    
    if file and is_safe_file(file.filename, file.read()):
        # Generate secure filename
        filename = secure_filename(file.filename)
        if len(filename) > MAX_FILENAME_LENGTH:
            abort(400, description="Filename too long")
            
        # Generate unique filename
        file_hash = hashlib.sha256(file.read()).hexdigest()
        file_extension = Path(filename).suffix
        unique_filename = f"{file_hash}{file_extension}"
        
        # Ensure upload directory exists and is secure
        UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        os.chmod(UPLOAD_FOLDER, 0o750)  # Restrict permissions
        
        # Save file
        file_path = UPLOAD_FOLDER / unique_filename
        file.save(file_path)
        
        # Verify file type after saving
        with open(file_path, 'rb') as f:
            file_type = magic.from_buffer(f.read(1024), mime=True)
            if file_type not in ['text/plain', 'application/pdf', 
                                'image/png', 'image/jpeg', 'image/gif']:
                os.remove(file_path)
                abort(400, description="Invalid file type")
        
        return "File uploaded successfully", 200
    else:
        abort(400, description="File type not allowed")