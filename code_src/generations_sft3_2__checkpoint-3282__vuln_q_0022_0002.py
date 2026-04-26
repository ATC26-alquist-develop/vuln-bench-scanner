import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
import magic
import hashlib

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = Path('/path/to/secure/upload/directory')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_hash(file_path: Path) -> str:
    """Calculate file hash for integrity check"""
    sha256_hash = hashlib.sha256()
    with file_path.open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route('/upload', methods=['POST'])
def upload_file() -> tuple:
    """Secure file upload handler"""
    # Check if the post request has the file part
    if 'file' not in request.files:
        abort(400, description="No file part in the request")
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        abort(400, description="No file selected")
    
    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Create file path
        file_path = UPLOAD_FOLDER / filename
        
        # Save file
        file.save(file_path)
        
        # Verify file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(str(file_path))
        
        if file_type.split('/')[0] not in ['text', 'image', 'application']:
            os.remove(file_path)
            abort(400, description="Invalid file type")
        
        # Verify file size
        if file_path.stat().st_size > MAX_CONTENT_LENGTH:
            os.remove(file_path)
            abort(413, description="File too large")
        
        # Calculate and store file hash
        file_hash = get_file_hash(file_path)
        
        # Return success with file info
        return {
            'filename': filename,
            'file_size': file_path.stat().st_size,
            'file_type': file_type,
            'file_hash': file_hash
        }, 200
        
    abort(400, description="File type not allowed")