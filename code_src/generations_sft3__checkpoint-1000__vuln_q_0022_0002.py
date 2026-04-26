import os
import secrets
from pathlib import Path
from typing import Optional
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
from werkzeug.datastructures import FileStorage
import magic

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = Path("/path/to/secure/upload/directory")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit

def is_safe_file(filename: str) -> bool:
    """Validate file extension and content type."""
    if not filename:
        return False
    
    # Secure filename
    filename = secure_filename(filename)
    
    # Check file extension
    if not '.' in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    
    # Validate file content
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(str(UPLOAD_FOLDER / filename))
    if file_type not in ['text/plain', 'application/pdf', 'image/png', 
                         'image/jpeg', 'image/gif']:
        return False
    
    return True

def generate_secure_filename(filename: str) -> str:
    """Generate a secure filename."""
    # Generate random token
    token = secrets.token_hex(16)
    # Combine with original filename
    return f"{token}_{filename}"

@app.route('/upload', methods=['POST'])
def upload_file() -> tuple[dict, int]:
    """Handle file upload securely."""
    if 'file' not in request.files:
        abort(400, description="No file part")
    
    file = request.files['file']
    
    if file.filename == '':
        abort(400, description="No selected file")
    
    if not is_safe_file(file.filename):
        abort(400, description="Invalid file type")
    
    if file:
        try:
            # Generate secure filename
            filename = generate_secure_filename(file.filename)
            
            # Save file
            file_path = UPLOAD_FOLDER / filename
            file.save(file_path)
            
            # Set secure permissions
            os.chmod(file_path, 0o644)
            
            return {"message": "File uploaded successfully"}, 200
            
        except Exception as e:
            # Log error securely (implement proper logging)
            app.logger.error(f"File upload error: {str(e)}")
            abort(500, description="Internal server error")
            
    return {"message": "File upload failed"}, 400

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.run(debug=False)