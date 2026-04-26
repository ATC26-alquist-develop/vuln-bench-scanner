from flask import Flask, request, send_from_directory, redirect, url_for, flash
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <head><title>File Upload</title></head>
    <body>
        <h1>Upload a file</h1>
        <form method="post" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        <h2>Files available for download:</h2>
        <ul>
            {% for file in files %}
                <li><a href="{{ url_for('download', filename=file) }}">{{ file }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        logging.info(f'File uploaded: {filename}')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string('''
    <!doctype html>
    <html>
    <head><title>File List</title></head>
    <body>
        <h1>Files available for download:</h1>
        <ul>
            {% for file in files %}
                <li><a href="{{ url_for('download', filename=file) }}">{{ file }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    ''', files=files)

if __name__ == '__main__':
    app.run(debug=True)