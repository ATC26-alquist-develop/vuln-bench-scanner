import os
from flask import Flask, request, send_file, abort
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler
import magic
import hashlib

app = Flask(__name__)

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Configure upload settings
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
        # Generate a unique filename
        file_hash = hashlib.sha256(file.read()).hexdigest()
        file.seek(0)  # Reset file pointer after reading
        unique_filename = f"{file_hash}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        
        # Verify file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        if file_type.split('/')[0] not in ['text', 'image', 'application']:
            os.remove(file_path)
            app.logger.error(f'Invalid file type: {file_type}')
            return 'Invalid file type', 400
        
        app.logger.info(f'File uploaded successfully: {unique_filename}')
        return 'File uploaded successfully', 200
    
    app.logger.warning('Allowed file type not found')
    return 'Allowed file type not found', 400

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        app.logger.warning(f'File not found: {filename}')
        abort(404)
    
    # Verify file type again
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    if file_type.split('/')[0] not in ['text', 'image', 'application']:
        app.logger.error(f'Invalid file type during download: {file_type}')
        abort(500)
    
    app.logger.info(f'File downloaded: {filename}')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=False)