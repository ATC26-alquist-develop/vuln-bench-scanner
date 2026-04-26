from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.csrf import CSRFProtect
import secrets
import re
from typing import Dict, Any
import bleach

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

class UserProfileForm(FlaskForm):
    """Form for validating user profile data"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=2, max=50)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    bio = StringField(
        'Bio',
        validators=[
            Length(max=500)
        ]
    )
    submit = SubmitField('Update Profile')

def sanitize_input(data: str) -> str:
    """Sanitize user input to prevent XSS"""
    return bleach.clean(data, tags=[], strip=True)

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    """Handle user profile page"""
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    form = UserProfileForm()
    
    if form.validate_on_submit():
        # Sanitize and validate form data
        name = sanitize_input(form.name.data)
        email = sanitize_input(form.email.data)
        bio = sanitize_input(form.bio.data)
        
        # Update user profile (implement database update here)
        # ...
        
        return redirect('/profile')
    
    # Fetch user profile data from database
    # user_data = fetch_user_data(user_id)
    # form.name.data = user_data.get('name', '')
    # form.email.data = user_data.get('email', '')
    # form.bio.data = user_data.get('bio', '')
    
    return render_template('profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)