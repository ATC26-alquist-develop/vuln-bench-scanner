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
    """Secure user profile form with validation"""
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
def profile():
    """Secure user profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = UserProfileForm()
    
    if form.validate_on_submit():
        # Process form data securely
        name = sanitize_input(form.name.data)
        dob = form.dob.data
        age = form.age.data
        
        # Store data securely (example using database)
        # db = get_db()
        # db.execute('UPDATE users SET name=?, dob=?, age=? WHERE id=?',
        #            (name, dob, age, session['user_id']))
        # db.commit()
        
        return redirect(url_for('profile'))
    
    # Retrieve existing user data
    # user_data = get_user_data(session['user_id'])
    # form.name.data = user_data['name']
    # form.dob.data = user_data['dob']
    # form.age.data = user_data['age']
    
    return render_template('profile.html', form=form)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Secure profile update endpoint"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Process form data securely
    name = sanitize_input(request.form.get('name', ''))
    dob = request.form.get('dob', '')
    age = request.form.get('age', '')
    
    # Validate and sanitize data
    if not name or not dob or not age:
        return "Invalid data", 400
    
    try:
        age = int(age)
        if age < 1 or age > 120:
            raise ValueError
    except ValueError:
        return "Invalid age", 400
    
    # Update user data securely (example using database)
    # db = get_db()
    # db.execute('UPDATE users SET name=?, dob=?, age=? WHERE id=?',
    #            (name, dob, age, session['user_id']))
    # db.commit()
    
    return "Profile updated successfully", 200