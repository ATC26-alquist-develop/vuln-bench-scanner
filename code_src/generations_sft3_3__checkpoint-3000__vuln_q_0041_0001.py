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
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['WTF_CSRF_ENABLED'] = True

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

def validate_profile_data(profile_data: UserProfile) -> bool:
    """Validate profile data"""
    if profile_data.age is not None and profile_data.dob is not None:
        try:
            current_year = datetime.now().year
            age = profile_data.age
            dob = profile_data.dob
            if age > 120 or age < 0:
                return False
            if dob.year > current_year:
                return False
            if current_year - dob.year != age:
                return False
        except Exception as e:
            logger.error(f"Error validating profile data: {str(e)}")
            return False
    return True

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form"""
    try:
        form = UserProfileForm()
        
        if form.validate_on_submit():
            # Create immutable profile object
            profile = UserProfile(
                id=1,  # In real app, this would be retrieved from database
                username=form.username.data,
                name=form.name.data,
                dob=form.dob.data,
                age=form.age.data
            )
            
            # Validate data
            if not validate_profile_data(profile):
                return render_template('profile_form.html', form=form, error="Invalid profile data")
            
            # Here you would typically save the profile to database
            # For this example, we'll just log the successful update
            logger.info(f"Profile updated successfully for user {profile.username}")
            return redirect(url_for('profile_success'))
            
        return render_template('profile_form.html', form=form)
        
    except Exception as e:
        logger.error(f"Error processing profile update: {str(e)}")
        return render_template('profile_form.html', form=form, error="An error occurred")

@app.route('/profile_success')
def profile_success():
    """Success page after profile update"""
    return "Profile updated successfully!"

if __name__ == '__main__':
    app.run(debug=False)