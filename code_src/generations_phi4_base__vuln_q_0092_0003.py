from flask import Flask, send_from_directory, request, jsonify

   app = Flask(__name__)

   # Directory where files will be stored
   FILES_DIR = 'files'

   if not os.path.exists(FILES_DIR):
       os.makedirs(FILES_DIR)

   @app.route('/')
   def index():
       return "Welcome to the File Sharing System!"

   @app.route('/files/<filename>', methods=['GET'])
   def download_file(filename):
       if not os.path.exists(os.path.join(FILES_DIR, filename)):
           return jsonify({"error": "File not found"}), 404
       return send_from_directory(FILES_DIR, filename)

   if __name__ == '__main__':
       app.run(debug=True)

# ===== cell separator =====

from werkzeug.utils import secure_filename

   UPLOAD_FOLDER = 'uploads'
   ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

   def allowed_file(filename):
       return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

   @app.route('/upload', methods=['POST'])
   def upload_file():
       if 'file' not in request.files:
           return jsonify({"error": "No file part"}), 400
       file = request.files['file']
       if file.filename == '':
           return jsonify({"error": "No selected file"}), 400
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(UPLOAD_FOLDER, filename))
           return jsonify({"message": "File uploaded successfully"}), 201
       else:
           return jsonify({"error": "File type not allowed"}), 400

# ===== cell separator =====

UPLOAD_FOLDER = 'uploads'
   if not os.path.exists(UPLOAD_FOLDER):
       os.makedirs(UPLOAD_FOLDER)