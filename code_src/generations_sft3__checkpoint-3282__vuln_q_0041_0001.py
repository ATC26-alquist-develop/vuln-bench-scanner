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
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure secret key generation
app.config['WTF_CSRF_ENABLED'] = True  # CSRF protection

class UserProfileForm(FlaskForm):
    """Form for updating user profile"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(max=100),
            Regexp(
                r'^[a-zA-Z\s]{1,50}$',
                message='Name must be 1-50 alphanumeric characters or spaces'
            )
        ]
    )
    dob = DateField(
        'Date of Birth',
        validators=[DataRequired()]
    )
    age = IntegerField(
        'Age',
        validators=[DataRequired()]
    )

def validate_profile_data(profile_data: UserProfile) -> bool:
    """Validate profile data"""
    if not (18 <= profile_data.age <= 100):
        return False
    if profile_data.dob > datetime.now():
        return False
    return True

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form"""
    form = UserProfileForm()
    
    if form.validate_on_submit():
        try:
            # Create immutable profile object
            profile = UserProfile(
                id=1,  # In real app, get this from database
                username=form.username.data,
                name=form.name.data,
                dob=form.dob.data,
                age=form.age.data
            )
            
            # Validate data
            if not validate_profile_data(profile):
                return render_template('profile_form.html', 
                                      form=form,
                                      error="Invalid profile data")
            
            # In real app, update database here
            logger.info(f"Profile updated successfully for user {profile.username}")
            return redirect(url_for('profile'))
            
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            return render_template('profile_form.html', 
                                  form=form,
                                  error="An error occurred while updating your profile")
    
    return render_template('profile_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode off in production