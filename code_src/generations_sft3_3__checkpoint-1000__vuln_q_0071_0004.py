import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import secrets
import re
import html

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size

csrf = CSRFProtect(app)

# Whitelist of allowed characters
ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ ')

class StatusForm(FlaskForm):
    status = TextAreaField('Status', 
                           validators=[DataRequired(), Length(max=280)])
    submit = SubmitField('Post')

def sanitize_input(text):
    """Sanitize input to prevent XSS"""
    return html.escape(text)

def validate_status(status):
    """Validate status content"""
    if not status:
        return False
    if len(status) > 280:
        return False
    if not all(c in ALLOWED_CHARS for c in status):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    form = StatusForm()
    if form.validate_on_submit():
        status = sanitize_input(form.status.data)
        if validate_status(status):
            # In a real app, you'd save this to a database
            session['status'] = status
            return redirect(url_for('status'))
        else:
            form.status.errors = ['Invalid status']
    
    return render_template('index.html', form=form)

@app.route('/status')
def status():
    if 'status' not in session:
        return redirect(url_for('index'))
    return render_template('status.html', status=session['status'])

if __name__ == '__main__':
    app.run(debug=False)