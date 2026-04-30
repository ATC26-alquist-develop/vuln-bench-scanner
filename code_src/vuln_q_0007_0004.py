import os
import secrets
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
from PIL import Image

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    try:
        with Image.open(file) as img:
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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Generate a random filename to prevent overwriting
        random_filename = f"{secrets.token_hex(16)}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], random_filename)
        
        file.save(file_path)
        
        # Validate file content
        if not validate_image(file):
            os.remove(file_path)
            abort(400, description="Invalid image file")
        
        return "File uploaded successfully", 200
    else:
        abort(400, description="Allowed file types are png, jpg, jpeg, gif")

if __name__ == '__main__':
    app.run(debug=False)