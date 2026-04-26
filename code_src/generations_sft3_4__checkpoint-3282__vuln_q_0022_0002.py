import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
import magic
import secrets

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = Path('/path/to/secure/upload/directory')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit

def is_safe_file(filename):
    """Validate file extension and size"""
    if not allowed_file(filename):
        return False
    
    # Check file size
    file_size = len(request.files['file'].read())
    if file_size > MAX_CONTENT_LENGTH:
        return False
    
    return True

def allowed_file(filename):
    """Check if file extension is allowed"""
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
    
    if file and is_safe_file(file.filename):
        # Generate secure random filename
        filename = secrets.token_hex(16)
        extension = Path(file.filename).suffix
        secure_name = f"{filename}{extension}"
        
        # Save file to secure location
        file_path = UPLOAD_FOLDER / secure_name
        file.save(file_path)
        
        # Verify file type
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(str(file_path))
        if file_mime.split('/')[0] not in ['text', 'image', 'application']:
            os.remove(file_path)
            abort(400, description="Invalid file type")
        
        return "File uploaded successfully", 200
    else:
        abort(400, description="File type not allowed")