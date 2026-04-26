from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.csrf import CSRFProtect
import secrets
import re
from datetime import datetime
import logging
from typing import Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserProfileForm(FlaskForm):
    """Form for updating user profile information"""
    username = StringField('Username', 
                          validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', 
                        validators=[DataRequired(), Length(max=100)])
    dob = DateField('Date of Birth', 
                    validators=[DataRequired()])
    age = IntegerField('Age', 
                      validators=[DataRequired(), NumberRange(min=18, max=120)])

def validate_input(form_data: UserProfileForm) -> bool:
    """Validate all form inputs"""
    errors = []
    
    # Validate username
    if not re.match(r'^[a-zA-Z0-9_]{3,50}$', form_data.username.data):
        errors.append('Invalid username format')
    
    # Validate email
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 
                   form_data.email.data):
        errors.append('Invalid email format')
    
    # Validate date of birth
    if form_data.dob.data > datetime.now().date():
        errors.append('Invalid date of birth')
    
    # Validate age
    if form_data.age.data < 18 or form_data.age.data > 120:
        errors.append('Age must be between 18 and 120')
    
    return len(errors) == 0

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form"""
    form = UserProfileForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Process form data securely
            username = form.username.data
            email = form.email.data
            dob = form.dob.data
            age = form.age.data
            
            # Store data securely (implement database operations here)
            # Example: db.update_user_profile(username, email, dob, age)
            
            logger.info(f"Profile updated successfully for user: {username}")
            return redirect(url_for('profile'))
        else:
            logger.warning(f"Invalid form data submitted: {form.errors}")
            return render_template('update_profile.html', form=form)
    
    return render_template('update_profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)