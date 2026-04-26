import os
from flask import Flask, request, send_file, abort, render_template_string
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=10)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# Configure upload settings
UPLOAD_FOLDER = '/tmp/secure_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
                app.logger.error(f'File upload failed: {str(e)}')
                return 'File upload failed', 500
        else:
            app.logger.warning('Invalid file type uploaded')
            return 'Invalid file type', 400
    
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if not os.path.exists(file_path):
        app.logger.warning(f'File not found: {filename}')
        abort(404)
    
    try:
        app.logger.info(f'Downloading file: {filename}')
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        app.logger.error(f'Download failed: {str(e)}')
        abort(500)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=False)