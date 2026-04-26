import os
from flask import Flask, request, send_file, abort
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure logging
log_file = 'app.log'
max_log_size = 10 * 1024 * 1024  # 10 MB
backup_count = 5

handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Configure upload settings
UPLOAD_FOLDER = '/tmp/secure_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

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
        
        try:
            file.save(file_path)
            app.logger.info(f'File uploaded successfully: {filename}')
            return 'File uploaded successfully', 200
        except Exception as e:
            app.logger.error(f'Error uploading file: {str(e)}')
            return 'Error uploading file', 500
    else:
        app.logger.warning(f'Invalid file type: {file.filename}')
        return 'Invalid file type', 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if not os.path.exists(file_path):
        app.logger.warning(f'File not found: {filename}')
        abort(404)
    
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        app.logger.error(f'Error downloading file: {str(e)}')
        abort(500)

if __name__ == '__main__':
    app.run(debug=False)