import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
import magic
import hashlib
import secrets

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = Path('/path/to/secure/upload/directory')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit
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
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        abort(400, description="No file part in the request")
        
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        abort(400, description="No file selected")
        
    if file and is_safe_file(file.filename, file.read()):
        # Generate secure filename
        filename = secure_filename(file.filename)
        if len(filename) > MAX_FILENAME_LENGTH:
            abort(400, description="Filename too long")
            
        # Generate random filename
        random_filename = secrets.token_hex(16) + Path(filename).suffix
        file_path = UPLOAD_FOLDER / random_filename
        
        # Save file
        try:
            file.save(file_path)
            
            # Verify file type after saving
            with open(file_path, 'rb') as f:
                file_content = f.read()
                if not is_safe_file(random_filename, file_content):
                    os.remove(file_path)
                    abort(400, description="Invalid file content")
                    
            return "File uploaded successfully", 200
            
        except Exception as e:
            # Clean up on error
            if file_path.exists():
                os.remove(file_path)
            abort(500, description="File upload failed")
            
    else:
        abort(400, description="File type not allowed")