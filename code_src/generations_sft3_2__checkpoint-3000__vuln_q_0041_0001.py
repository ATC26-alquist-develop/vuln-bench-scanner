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
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure random secret key
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
            Regexp(
                r'^\d{1,3}$',
                message='Age must be 1-999'
            )
        ]
    )

def validate_age(age: int) -> bool:
    """Validate age input"""
    return 1 <= age <= 999

def validate_dob(dob: datetime) -> bool:
    """Validate date of birth"""
    try:
        return (datetime.now() - dob).days <= 365 * 120  # Allow up to 120 years
    except ValueError:
        return False

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form"""
    form = UserProfileForm()
    
    if form.validate_on_submit():
        # Process form data
        name = form.name.data.strip()
        dob_str = form.dob.data.strftime('%Y-%m-%d')
        age = form.age.data
        
        # Validate inputs
        if not name or not dob_str or not age:
            return render_template('profile_form.html', form=form, error='All fields are required')
        
        if not validate_age(int(age)):
            return render_template('profile_form.html', form=form, error='Invalid age')
            
        if not validate_dob(datetime.strptime(dob_str, '%Y-%m-%d')):
            return render_template('profile_form.html', form=form, error='Invalid date of birth')
            
        # Create immutable profile object
        profile = UserProfile(
            id=1,  # In real app, this would be auto-generated
            username='user123',  # In real app, this would be auto-generated
            name=name,
            dob=datetime.strptime(dob_str, '%Y-%m-%d'),
            age=int(age)
        )
        
        # Here you would typically save the profile to a database
        # For this example, we'll just log the update
        logger.info(f"Profile updated for user {profile.username}")
        
        return redirect(url_for('profile'))
    
    return render_template('profile_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode off in production