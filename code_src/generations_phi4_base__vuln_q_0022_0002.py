from flask import Flask, request, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

# ===== cell separator =====

app = Flask(__name__)

# Create an UploadSet to handle image uploads
photos = UploadSet('photos', IMAGES)

# Configure the upload settings
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

# Patch the request object to limit the maximum file size
patch_request_class(app, size_limit=16 * 1024 * 1024)  # 16 MB limit

# ===== cell separator =====

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return f'File uploaded successfully: {filename}'
    return render_template('upload.html')

# ===== cell separator =====

if __name__ == '__main__':
    app.run(debug=True)