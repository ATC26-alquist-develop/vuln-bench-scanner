import os
import secrets

UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.chmod(UPLOAD_FOLDER, 0o700)  # Restrict permissions

# ===== cell separator =====

import os
from werkzeug.utils import secure_filename
import magic

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_file_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Generate a random filename to prevent overwriting
        random_filename = secrets.token_hex(16)
        file_path = os.path.join(UPLOAD_FOLDER, random_filename)
        
        file.save(file_path)
        
        # Verify file type
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(file_path)
        if file_mime.split('/')[0] not in ['text', 'image', 'application']:
            os.remove(file_path)
            return None
            
        return file_path
    return None

# ===== cell separator =====

from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        file_path = secure_file_upload(file)
        if file_path:
            return redirect(url_for('success', filename=file_path))
        else:
            return 'Invalid file type', 400
    
    return 'Invalid file type', 400

@app.route('/success/<filename>')
def success(filename):
    return f'File uploaded successfully: {filename}'