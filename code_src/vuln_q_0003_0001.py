```python
import os
from pathlib import Path
from typing import Optional
from flask import Flask, request, send_file, abort, jsonify
import logging
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Secure configuration
UPLOAD_FOLDER = Path('/path/to/secure/upload/directory')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = UPLOAD_FOLDER / filename
            
            # Prevent overwriting existing files
            counter = 1
            while file_path.exists():
                name = f"{filename}_{counter}"
                file_path = UPLOAD_FOLDER / name
                counter += 1
            
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file.save(file_path)
            file_hash = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    file_hash.update(chunk)
            
            logging.info(f"File uploaded: {filename}, Hash: {file_hash.hexdigest()}")
            return jsonify({'message': 'File uploaded successfully', 'hash': file_hash.hexdigest()})
        
        return jsonify({'error': 'File type not allowed'}), 400
    
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/download/<filename>')
def download_file(filename: str):
    try:
        file_path = UPLOAD_FOLDER / filename
        
        if not file_path.exists():
            abort(404)
        
        logging.info(f"File downloaded: {filename}")
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        logging.error(f"Error downloading file: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False)
```


This implementation includes several security measures:

1. Input validation: We use `secure_filename()` to sanitize filenames and validate file types.
2. File size limit: We set a maximum file size to prevent denial-of-service attacks.
3. Secure file storage: Files are stored in a designated secure directory outside the web root.
4. Error handling: We use try-except blocks to catch and log errors without exposing sensitive information.
5. Logging: We implement basic logging for file operations.
6. File integrity: We generate a SHA-256 hash of uploaded files for verification.
7. No overwriting: We prevent overwriting existing files by appending a counter to filenames.
8. HTTPS: While not explicitly shown, it's assumed that this app would be deployed with HTTPS in production.
9.