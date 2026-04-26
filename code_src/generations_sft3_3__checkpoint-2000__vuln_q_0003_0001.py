import os
from flask import Flask, request, send_file, abort
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler
import magic
import hashlib

app = Flask(__name__)

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = 'app.log'
log_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=10)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# Configure upload settings
UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit

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
        app.logger.warning('No file part in the request')
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        app.logger.warning('No selected file')
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(file_path)
        
        # Verify file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        if file_type.split('/')[0] not in ['text', 'image', 'application']:
            os.remove(file_path)
            app.logger.warning(f'Invalid file type: {file_type} for {filename}')
            return 'Invalid file type', 400
        
        # Calculate file hash
        file_hash = get_file_hash(file_path)
        app.logger.info(f'File uploaded: {filename}, Hash: {file_hash}')
        return 'File uploaded successfully', 200
    
    app.logger.warning('Allowed file type not found')
    return 'Allowed file type not found', 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if not os.path.exists(file_path):
        app.logger.warning(f'File not found: {filename}')
        abort(404)
    
    # Verify file type
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    if file_type.split('/')[0] not in ['text', 'image', 'application']:
        app.logger.warning(f'Invalid file type: {file_type} for {filename}')
        abort(400)
    
    app.logger.info(f'File downloaded: {filename}')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)