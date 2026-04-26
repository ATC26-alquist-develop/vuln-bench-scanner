import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
import magic
import secrets

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = Path('/tmp/secure_uploads')
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILENAME_LENGTH = 255

def is_safe_file(filename: str, file_content: bytes) -> bool:
    """Validate file extension and content type."""
    try:
        # Secure filename
        filename = secure_filename(filename)
        
        # Check file extension
        if not allowed_file(filename):
            return False
            
        # Check file size
        if len(file_content) > MAX_CONTENT_LENGTH:
            return False
            
        # Verify file content
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
        # Generate secure random filename
        original_filename = file.filename
        secure_filename = secrets.token_hex(16)
        
        # Save file
        file_path = UPLOAD_FOLDER / secure_filename
        file.save(file_path)
        
        # Verify file permissions
        os.chmod(file_path, 0o644)
        
        return f"File uploaded successfully as {secure_filename}", 200
    else:
        abort(400, description="File not allowed or too large")

if __name__ == '__main__':
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=False)