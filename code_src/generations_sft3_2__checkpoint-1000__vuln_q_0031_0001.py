from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.csrf import CSRFProtect
import secrets
import re
from datetime import datetime
import bleach

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

class UserProfileForm(FlaskForm):
    """Form for validating user profile data"""
    name = StringField('Name', 
                      validators=[DataRequired(), Length(max=100)])
    age = IntegerField('Age', 
                      validators=[DataRequired(), NumberRange(min=1, max=120)])
    dob = DateField('Date of Birth', 
                    validators=[DataRequired()])
    email = StringField('Email', 
                       validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', 
                       validators=[Length(max=20)])

def sanitize_input(data):
    """Sanitize user input to prevent XSS"""
    return bleach.clean(data, tags=[], strip=True)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Handle user profile page"""
    if 'user_id' not in session:
        return redirect('/login')
    
    form = UserProfileForm()
    
    if request.method == 'POST' and form.validate():
        # Sanitize all form fields
        name = sanitize_input(form.name.data)
        age = sanitize_input(form.age.data)
        dob = sanitize_input(form.dob.data)
        email = sanitize_input(form.email.data)
        phone = sanitize_input(form.phone.data)
        
        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "Invalid email format", 400
            
        # Process validated data (implement your database logic here)
        # ...
        
        return "Profile updated successfully", 200
    
    return render_template('profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)