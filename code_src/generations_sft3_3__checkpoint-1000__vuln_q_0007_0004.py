import os
import uuid
import magic
from werkzeug.utils import secure_filename
from flask import Flask, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Configure upload settings
UPLOAD_FOLDER = '/path/to/secure/upload/directory'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_type(file):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read(1024))
    file.seek(0)  # Reset file pointer
    return file_type.split('/')[0] in ['text', 'application', 'image']

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limiting
def upload_file():
    if 'file' not in request.files:
        abort(400, description="No file part")
    
    file = request.files['file']
    
    if file.filename == '':
        abort(400, description="No selected file")
    
    if file and allowed_file(file.filename):
        # Generate a secure random filename
        filename = secure_filename(str(uuid.uuid4()) + '_' + file.filename)
        
        # Validate file type
        if not validate_file_type(file):
            abort(400, description="Invalid file type")
        
        # Check file size
        if file.content_length > MAX_CONTENT_LENGTH:
            abort(413, description="File too large")
        
        # Secure file path
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save file
        file.save(file_path)
        
        return "File uploaded successfully", 200
    else:
        abort(400, description="File type not allowed")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS