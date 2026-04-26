import os
from flask import Flask, request, send_file, abort
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure upload directory
UPLOAD_FOLDER = '/tmp/secure_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ensure upload folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure upload settings
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
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
        file.save(file_path)
        app.logger.info(f'File uploaded: {filename}')
        return 'File uploaded successfully', 200
    else:
        app.logger.warning('Invalid file type uploaded')
        return 'Invalid file type', 400

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(file_path):
        app.logger.info(f'File downloaded: {filename}')
        return send_file(file_path, as_attachment=True)
    else:
        app.logger.warning(f'File not found: {filename}')
        abort(404)

if __name__ == '__main__':
    app.run(debug=False)