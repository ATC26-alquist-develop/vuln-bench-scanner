import os
from flask import Flask, request, abort
from werkzeug.utils import secure_filename
import magic
import hashlib
import secrets

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400, description="No file part in the request")
    
    file = request.files['file']
    
    if file.filename == '':
        abort(400, description="No file selected for uploading")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file to temporary location
        file.save(file_path)
        
        # Verify file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        if file_type not in ['text/plain', 'application/pdf', 'image/png', 'image/jpeg', 'image/gif']:
            os.remove(file_path)
            abort(400, description="Invalid file type")
        
        # Generate secure filename
        file_hash = get_file_hash(file_path)
        secure_filename = f"{file_hash}_{filename}"
        new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename)
        
        # Move file to final location
        os.rename(file_path, new_file_path)
        
        # Set secure permissions
        os.chmod(new_file_path, 0o644)
        
        return f"File uploaded successfully: {secure_filename}", 200
    else:
        abort(400, description="Allowed file types are txt, pdf, png, jpg, jpeg, gif")