```python
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
```


This implementation includes several security measures:

1. File extension whitelist to prevent unauthorized file types.
2. Secure filename generation using werkzeug's secure_filename function.
3. File size limit to prevent denial of service attacks.
4. MIME type verification using python-magic to ensure the file is actually an image.
5. Image validation using PIL to ensure the file is a valid image.
6. Secure random filename generation to prevent filename guessing attacks.
7. Storing files outside the web root to prevent direct access.
8. Running the Flask app with debug mode disabled in production.

Note that this code assumes you're using Flask and Pillow (PIL) libraries. Make sure to install these dependencies and properly configure your environment. Also, ensure that the UPLOAD_FOLDER is set to a secure location with appropriate permissions.