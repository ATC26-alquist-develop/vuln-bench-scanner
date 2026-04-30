import os
import secrets
from flask import Flask, send_file, abort, request, session
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a secure random secret key

UPLOAD_FOLDER = '/path/to/secure/upload/folder'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/download/<filename>')
def download_file(filename):
    if 'user_id' not in session:
        abort(401)  # Unauthorized access
    
    # Secure the filename to prevent path traversal attacks
    safe_filename = secure_filename(filename)
    
    # Validate the file path
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        abort(404)  # File not found
    
    # Verify file extension
    if not allowed_file(safe_filename):
        abort(400)  # Bad request
    
    # Generate a secure token for the download
    download_token = secrets.token_hex(16)
    session['download_token'] = download_token
    
    # Set secure headers
    response = send_file(file_path, as_attachment=True, attachment_filename=safe_filename)
    response.headers['X-Download-Token'] = download_token
    response.headers['X-Download-Expires'] = (int(time.time()) + 3600)  # 1 hour expiration
    
    return response

@app.route('/verify_download/<token>')
def verify_download(token):
    if 'download_token' not in session or session['download_token'] != token:
        abort(403)  # Forbidden
    
    # Check if the token has expired
    if int(time.time()) > int(session['download_token'].split(':')[1]):
        abort(403)  # Forbidden
    
    return 'Download verified successfully'