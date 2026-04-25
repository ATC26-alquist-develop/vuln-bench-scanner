import os
import secrets
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
import magic

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

def secure_file_upload():
    if 'file' not in request.files:
        abort(400, description="No file part in the request")
    
    file = request.files['file']
    
    if file.filename == '':
        abort(400, description="No file selected for uploading")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Generate a random filename to prevent overwriting
        random_filename = secrets.token_hex(16)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], random_filename)
        
        # Save the file
        file.save(file_path)
        
        # Verify file type
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(file_path)
        
        if file_mime.split('/')[0] not in ['text', 'image', 'application']:
            os.remove(file_path)
            abort(400, description="Invalid file type")
        
        return random_filename
    else:
        abort(400, description="File type not allowed")

@app.route('/upload', methods=['POST'])
def upload_file():
    return secure_file_upload()

if __name__ == '__main__':
    app.run(debug=False)