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
app.config['SESSION_COOKIE_SECURE'] = True  # Secure session cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes session timeout

class UserProfileForm(FlaskForm):
    """Form for validating user profile data"""
    name = StringField('Name', 
                      validators=[DataRequired(), Length(max=100)])
    dob = DateField('Date of Birth', 
                   validators=[DataRequired()])
    age = IntegerField('Age', 
                      validators=[DataRequired(), NumberRange(min=1, max=120)])

class UserProfileValidator:
    """Validate user profile data"""
    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate name format"""
        return bool(re.match(r'^[A-Za-z\s]{1,100}$', name))

    @staticmethod
    def validate_age(age: int) -> bool:
        """Validate age"""
        return 1 <= age <= 120

    @staticmethod
    def validate_dob(dob: datetime.date) -> bool:
        """Validate date of birth"""
        today = datetime.now().date()
        if dob:
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            return 1 <= age <= 120
        return False

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Handle user profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = UserProfileForm()
    if form.validate_on_submit():
        # Sanitize and validate input
        name = bleach.clean(form.name.data)
        dob = form.dob.data
        age = form.age.data

        # Validate all data
        if not UserProfileValidator.validate_name(name):
            form.name.errors.append("Invalid name format")
            return render_template('profile.html', form=form)

        if not UserProfileValidator.validate_age(age):
            form.age.errors.append("Invalid age")
            return render_template('profile.html', form=form)

        if not UserProfileValidator.validate_dob(dob):
            form.dob.errors.append("Invalid date of birth")
            return render_template('profile.html', form=form)

        # Update user profile (implement secure database update here)
        # ...

        return redirect(url_for('profile'))

    return render_template('profile.html', form=form)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Handle profile update via API"""
    if 'user_id' not in session:
        return {'error': 'Unauthorized'}, 401

    # Implement secure API endpoint here
    # ...

    return {'message': 'Profile updated successfully'}, 200