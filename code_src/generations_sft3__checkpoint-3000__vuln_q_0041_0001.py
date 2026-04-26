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
        validators=[
            DataRequired(),
            Regexp(
                r'^\d{1,3}$',
                message='Age must be 1-999'
            )
        ]
    )

def validate_age(age: int) -> bool:
    """Validate age input"""
    return 1 <= age <= 999

def validate_name(name: str) -> bool:
    """Validate name input"""
    return bool(re.match(r'^[a-zA-Z\s]{1,50}$', name))

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form"""
    form = UserProfileForm()
    
    if form.validate_on_submit():
        # Get validated data
        name = form.name.data
        dob = form.dob.data
        age = form.age.data
        
        # Validate age
        if not validate_age(age):
            logger.warning(f"Invalid age attempt: {age}")
            return render_template('profile_form.html', form=form, error="Invalid age")
            
        # Validate name
        if not validate_name(name):
            logger.warning(f"Invalid name attempt: {name}")
            return render_template('profile_form.html', form=form, error="Invalid name")
            
        # Create immutable profile object
        profile = UserProfile(
            id=1,  # In real app, would get this from database
            username="user123",  # In real app, would get this from database
            name=name,
            dob=dob,
            age=age
        )
        
        # Here you would save the profile to database
        logger.info(f"Profile updated successfully for user {profile.username}")
        return redirect(url_for('profile'))
    
    return render_template('profile_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)