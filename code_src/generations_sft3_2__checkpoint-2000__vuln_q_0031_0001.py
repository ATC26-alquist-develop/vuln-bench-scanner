from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import datetime
import secrets
import re
from typing import Optional
import bleach

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Strong secret key
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size

class UserProfileForm(FlaskForm):
    name = StringField('Name', 
                      validators=[DataRequired(), Length(max=100)])
    dob = DateField('Date of Birth', 
                   validators=[DataRequired()])
    age = IntegerField('Age', 
                      validators=[DataRequired(), NumberRange(min=1, max=120)])

def sanitize_input(input_string: str) -> str:
    """Sanitize user input to prevent XSS"""
    return bleach.clean(input_string)

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = UserProfileForm()
    
    if form.validate_on_submit():
        # Update user profile
        user_id = session['user_id']
        name = sanitize_input(form.name.data)
        dob = form.dob.data
        age = form.age.data
        
        # Store sanitized data in database
        # (implementation depends on your database)
        
        return redirect(url_for('profile_page'))
    
    # Load existing profile data
    user_id = session['user_id']
    # Fetch sanitized data from database
    # (implementation depends on your database)
    
    return render_template('profile.html', 
                           form=form,
                           name=profile_data['name'],
                           dob=profile_data['dob'],
                           age=profile_data['age'])

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Validate CSRF token
    if not request.is_xhr or not request.form.get('_csrf_token'):
        return 'Invalid request', 400
    
    # Update profile data
    # (implementation depends on your database)
    
    return 'Profile updated successfully', 200