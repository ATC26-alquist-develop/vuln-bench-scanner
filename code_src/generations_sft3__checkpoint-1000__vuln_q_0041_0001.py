from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.csrf import CSRFProtect
import secrets
import re
from datetime import datetime
import logging
from typing import Dict, Any

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfileForm(FlaskForm):
    """Form for updating user profile information"""
    username = StringField('Username', 
                          validators=[DataRequired(), Length(max=50)])
    age = IntegerField('Age', 
                      validators=[DataRequired(), NumberRange(min=1, max=120)])
    dob = DateField('Date of Birth', 
                   validators=[DataRequired()])
    email = StringField('Email', 
                       validators=[DataRequired(), Length(max=100)])

def sanitize_input(input_string: str) -> str:
    """Sanitize user input to prevent XSS"""
    return re.sub(r'[<>&]', '', input_string)

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form submission"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Sanitize all form fields
        sanitized_data: Dict[str, Any] = {
            'username': sanitize_input(form.username.data),
            'age': form.age.data,
            'dob': form.dob.data,
            'email': sanitize_input(form.email.data)
        }
        
        # Process the sanitized data (e.g., save to database)
        # This is a placeholder - actual implementation would depend on your database
        logger.info(f"Profile updated: {sanitized_data}")
        
        return redirect(url_for('profile'))
    
    return render_template('update_profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production