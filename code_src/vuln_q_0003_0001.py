from flask import Flask, request, send_file, abort
import os
import logging
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Configure upload settings
UPLOAD_FOLDER = '/tmp/secure_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logging.warning('No file part in the request')
        abort(400, description='No file part in the request')
    
    file = request.files['file']
    
    if file.filename == '':
        logging.warning('No file selected for uploading')
        abort(400, description='No file selected for uploading')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        logging.info(f'File uploaded: {unique_filename}')
        return 'File uploaded successfully', 200
    else:
        logging.warning('Invalid file type')
        abort(400, description='Invalid file type')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    if not os.path.exists(file_path):
        logging.warning(f'File not found: {filename}')
        abort(404, description='File not found')
    logging.info(f'File downloaded: {filename}')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)