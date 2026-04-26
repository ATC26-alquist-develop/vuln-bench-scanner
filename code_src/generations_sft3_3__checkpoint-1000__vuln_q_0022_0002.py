import os
import secrets
from pathlib import Path
from typing import Optional
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = Path("/path/to/secure/upload/directory")
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit

# Rate limiting to prevent abuse
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limit
def upload_file() -> tuple[str, int]:
    """Secure file upload endpoint."""
    if 'file' not in request.files:
        abort(400, description="No file part")
    
    file = request.files['file']
    
    if file.filename == '':
        abort(400, description="No selected file")
    
    if file and allowed_file(file.filename):
        # Generate secure random filename
        filename = secure_filename(file.filename)
        # Ensure filename is unique
        counter = 1
        while (UPLOAD_FOLDER / filename).exists():
            filename = f"{filename}_{counter}"
            counter += 1
        
        # Generate random filename extension
        ext = os.path.splitext(filename)[1]
        secure_filename = f"{secrets.token_hex(16)}{ext}"
        
        # Save file
        file_path = UPLOAD_FOLDER / secure_filename
        file.save(file_path)
        
        return f"File uploaded successfully: {secure_filename}", 200
    
    abort(400, description="File type not allowed")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS