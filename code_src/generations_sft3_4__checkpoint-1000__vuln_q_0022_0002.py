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
@limiter.limit("10 per minute")  # Rate limiting
def upload_file() -> tuple[Optional[str], int]:
    """Secure file upload endpoint."""
    if 'file' not in request.files:
        abort(400, description="No file part")
    
    file = request.files['file']
    
    if file.filename == '':
        abort(400, description="No selected file")
    
    if file and allowed_file(file.filename):
        try:
            # Generate secure random filename
            filename = secure_filename(file.filename)
            # Generate a random filename to prevent overwriting
            random_filename = f"{secrets.token_hex(16)}{Path(filename).suffix}"
            file_path = UPLOAD_FOLDER / random_filename
            
            # Save file securely
            file.save(file_path)
            
            # Set secure permissions
            os.chmod(file_path, 0o644)
            
            return "File uploaded successfully", 200
            
        except Exception as e:
            # Log error securely (implement proper logging)
            app.logger.error(f"Upload error: {str(e)}")
            abort(500, description="Internal server error")
            
    abort(400, description="File type not allowed")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS