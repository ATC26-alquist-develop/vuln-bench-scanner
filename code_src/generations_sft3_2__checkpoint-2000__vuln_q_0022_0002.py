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
UPLOAD_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif'}

def is_safe_file(filename: str) -> bool:
    """Validate file extension and size."""
    # Check file extension
    if not allowed_file(filename):
        return False
    
    # Check file size
    file_size = len(request.files['file'].read())
    if file_size > MAX_CONTENT_LENGTH:
        return False
    
    return True

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in UPLOAD_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file() -> tuple:
    """Secure file upload endpoint."""
    if 'file' not in request.files:
        abort(400, description="No file part in the request")
    
    file = request.files['file']
    
    if file.filename == '':
        abort(400, description="No file selected")
    
    if not is_safe_file(file.filename):
        abort(400, description="Invalid file type or size")
    
    # Secure filename
    filename = secure_filename(file.filename)
    
    # Generate unique filename
    file_hash = hashlib.sha256(file.read()).hexdigest()
    unique_filename = f"{file_hash}{os.path.splitext(filename)[1]}"
    
    # Ensure upload directory exists
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_path = UPLOAD_FOLDER / unique_filename
    file.save(file_path)
    
    # Verify file type using libmagic
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(str(file_path))
    
    if file_type not in ['text/plain', 'application/pdf', 'image/png', 'image/jpeg', 'image/gif']:
        os.remove(file_path)
        abort(400, description="Invalid file type")
    
    return {"message": "File uploaded successfully"}, 200