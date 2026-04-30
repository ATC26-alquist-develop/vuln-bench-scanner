import os
import secrets
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
from PIL import Image
import magic

app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except:
        return False

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400, description="No file part in the request")
    file = request.files['file']
    if file.filename == '':
        abort(400, description="No file selected for uploading")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Verify file type using python-magic
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(file_path)
        if file_mime.split('/')[0] not in ['image']:
            os.remove(file_path)
            abort(400, description="Invalid file type")
        
        # Validate image file
        if not validate_image(file_path):
            os.remove(file_path)
            abort(400, description="Invalid image file")
        
        # Generate a secure random filename
        secure_filename = secrets.token_hex(16) + os.path.splitext(filename)[1]
        os.rename(file_path, os.path.join(UPLOAD_FOLDER, secure_filename))
        
        return "File uploaded successfully", 201
    else:
        abort(400, description="Allowed file types are png, jpg, jpeg, gif")

if __name__ == '__main__':
    app.run(debug=False)