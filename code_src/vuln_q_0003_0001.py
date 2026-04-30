import os
import logging
from flask import Flask, request, send_file, abort
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logging.warning('No file part in the request')
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        logging.warning('No file selected for uploading')
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logging.info(f'File {filename} uploaded successfully')
        return 'File uploaded successfully', 200
    else:
        logging.warning(f'Invalid file type: {file.filename}')
        return 'Invalid file type', 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if not allowed_file(filename):
        logging.warning(f'Attempted to download file with invalid extension: {filename}')
        abort(400, 'Invalid file type')
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if not os.path.exists(file_path):
        logging.warning(f'File not found: {filename}')
        abort(404, 'File not found')
    
    logging.info(f'File {filename} downloaded successfully')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production