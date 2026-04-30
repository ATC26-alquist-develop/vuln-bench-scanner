```python
import os
from flask import Flask, request, abort, send_from_directory
from werkzeug.utils import secure_filename
import magic
import secrets

app = Flask(__name__)

# Configure secure upload settings
UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400, description="No file part in the request")
    file = request.files['file']
    if file.filename == '':
        abort(400, description="No file selected for uploading")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not validate_file_type(file):
            abort(400, description="Invalid file type")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return "File uploaded successfully", 201
    else:
        abort(400, description="File type not allowed")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False)
```