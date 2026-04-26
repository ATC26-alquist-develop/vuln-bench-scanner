from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp
from datetime import datetime
import secrets
import re
from typing import Optional
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    """Immutable user profile data"""
    id: int
    username: str
    name: str
    dob: datetime
    age: int

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Strong secret key
app.config['WTF_CSRF_ENABLED'] = True  # CSRF protection

class UserProfileForm(FlaskForm):
    """Form for updating user profile"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Name is required'),
            Length(max=100, message='Name must be 100 characters or less'),
            Regexp(
                r'^[a-zA-Z\s]{1,50}$',
                message='Name must contain only letters and spaces'
            )
        ]
    )
    dob = DateField(
        'Date of Birth',
        validators=[DataRequired(message='Date of Birth is required')]
    )
    age = IntegerField(
        'Age',
        validators=[
            DataRequired(message='Age is required'),
            lambda form, field: field.data >= 0,
            lambda form, field: field.data <= 150
        ]
    )

def validate_input(name: str, dob: datetime, age: int) -> bool:
    """Validate user input"""
    if not name or not isinstance(name, str):
        return False
    if not isinstance(dob, datetime):
        return False
    if not isinstance(age, int):
        return False
    if age < 0 or age > 150:
        return False
    if len(name) > 100:
        return False
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob.strftime('%Y-%m-%d')):
        return False
    return True

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form"""
    form = UserProfileForm()
    
    if form.validate_on_submit():
        # Validate input
        name = form.name.data
        dob = form.dob.data
        age = form.age.data
        
        if not validate_input(name, dob, age):
            form.name.errors.append('Invalid input')
            return render_template('update_profile.html', form=form)
            
        # Here you would typically:
        # 1. Update the database with the new profile data
        # 2. Set a success message
        # 3. Redirect to profile page
        
        logger.info(f"Profile updated successfully for user {name}")
        return redirect(url_for('profile'))
    
    return render_template('update_profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode off in production