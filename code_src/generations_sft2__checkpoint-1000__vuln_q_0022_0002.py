from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import magic
import hashlib
from datetime import datetime
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

def validate_file_type(file):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read(1024))
    file.seek(0)  # Reset file pointer
    return file_type.split('/')[0] in ['text', 'application', 'image']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            return 'No file part', 400
        
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file', 400
        
        if file and allowed_file(file.filename):
            # Secure filename
            filename = secure_filename(file.filename)
            
            # Generate unique filename
            file_extension = os.path.splitext(filename)[1]
            unique_filename = f"{secrets.token_hex(16)}{file_extension}"
            
            # Create secure path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(file_path)
            
            # Validate file type
            if not validate_file_type(file):
                os.remove(file_path)
                return 'Invalid file type', 400
            
            # Generate hash for integrity check
            file_hash = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    file_hash.update(chunk)
            
            # Store hash (in real app, use secure database)
            # For this example, we'll just print it
            print(f"File hash: {file_hash.hexdigest()}")
            
            return 'File uploaded successfully', 200
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=False)