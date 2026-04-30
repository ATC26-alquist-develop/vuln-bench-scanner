import os
import secrets
from flask import Flask, request, send_file, abort, jsonify
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure secure upload settings
UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Set secure permissions for upload directory
os.chmod(UPLOAD_FOLDER, 0o700)

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.warning('No file part in the request')
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        app.logger.warning('No file selected for uploading')
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        app.logger.info(f'File uploaded successfully: {filename}')
        return jsonify({'message': 'File uploaded successfully'}), 200
    
    app.logger.warning('Invalid file type attempted to be uploaded')
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        app.logger.warning(f'Attempted to download non-existent file: {filename}')
        abort(404)
    
    if not allowed_file(filename):
        app.logger.warning(f'Attempted to download file with invalid extension: {filename}')
        abort(400)
    
    app.logger.info(f'File downloaded successfully: {filename}')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)