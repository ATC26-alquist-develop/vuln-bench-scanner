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
    """Secure form for updating profile information"""
    username = StringField('Username', 
                          validators=[DataRequired(), Length(max=50)])
    age = IntegerField('Age', 
                      validators=[DataRequired(), NumberRange(min=1, max=120)])
    dob = DateField('Date of Birth', 
                   validators=[DataRequired()])
    email = StringField('Email', 
                       validators=[DataRequired(), Length(max=100)])
    
    def validate_email(self, field: StringField) -> None:
        """Validate email format"""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', field.data):
            raise ValueError("Invalid email format")

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize input data to prevent injection attacks"""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = value.strip()
        elif isinstance(value, (int, float)):
            sanitized[key] = int(value)  # Convert to int for numeric fields
        elif isinstance(value, datetime):
            sanitized[key] = value.isoformat()
        else:
            sanitized[key] = value  # Keep other types as is
    return sanitized

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    """Handle profile update form"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Sanitize and validate all form fields
        sanitized_data = sanitize_input({
            'username': form.username.data,
            'age': form.age.data,
            'dob': form.dob.data,
            'email': form.email.data
        })
        
        # Process the sanitized data (e.g., update database)
        # This is a placeholder - actual implementation would depend on your database
        logger.info(f"Profile updated: {sanitized_data}")
        
        return redirect(url_for('profile'))
    
    return render_template('profile_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production