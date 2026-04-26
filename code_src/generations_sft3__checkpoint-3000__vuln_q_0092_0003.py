import os
from pathlib import Path
from typing import Optional
from werkzeug.utils import secure_filename
from flask import Flask, send_file, abort
from flask_login import login_required, current_user

app = Flask(__name__)

@app.route('/download/<path:filename>')
@login_required
def download_file(filename: str) -> Optional[bytes]:
    """
    Securely download a file from the server.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        File content if valid, None if file doesn't exist or access is denied
    """
    try:
        # Sanitize filename to prevent path traversal
        safe_filename = secure_filename(filename)
        
        # Construct full path
        file_path = Path(app.config['UPLOAD_FOLDER']) / safe_filename
        
        # Verify file exists and is within allowed directory
        if not file_path.exists() or not file_path.is_file():
            abort(404)
            
        # Check if user has permission to access this file
        if not current_user.can_access_file(file_path):
            abort(403)
            
        # Send file securely
        return send_file(
            file_path,
            as_attachment=True,
            download_name=safe_filename
        )
        
    except Exception as e:
        app.logger.error(f"Error during file download: {str(e)}")
        abort(500)