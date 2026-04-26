import os
from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import secrets
import bleach
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
app.config['UPLOAD_FOLDER'] = 'secure_uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Whitelist of allowed characters for status updates
ALLOWED_CHARS = re.compile(r'^[a-zA-Z0-9@._-]+$')

class StatusForm(FlaskForm):
    status = TextAreaField('Status', validators=[
        DataRequired(),
        Length(max=280),
        # Sanitize input to allow only safe characters
        lambda form, field: ALLOWED_CHARS.match(field.data) is not None
    ])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    form = StatusForm()
    if form.validate_on_submit():
        # Sanitize and validate status update
        status = bleach.clean(form.status.data)
        
        # Generate unique filename
        filename = secrets.token_hex(16)
        file_extension = os.path.splitext(form.file.data.filename)[1]
        safe_filename = f"{filename}{file_extension}"
        
        # Save file securely
        if form.file.data:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            form.file.data.save(file_path)
        
        # Store status in database (simplified for example)
        # In production, use a proper database with proper security measures
        
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode off in production