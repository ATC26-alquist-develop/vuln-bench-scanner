from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.csrf import CSRFProtect
import secrets
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=12),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm New Password')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        # In a real application, you would retrieve the user's ID from a session or token
        user_id = 1  # Placeholder - replace with actual user ID retrieval
        
        # Retrieve the old password from the database
        old_password = get_old_password_from_db(user_id)
        
        # Verify the old password
        if check_password_hash(old_password, form.old_password.data):
            # Hash the new password
            new_password_hash = generate_password_hash(form.new_password.data)
            
            # Update the password in the database
            update_password_in_db(user_id, new_password_hash)
            
            return redirect(url_for('password_changed'))
        else:
            form.old_password.errors.append('Invalid old password')
    
    return render_template('change_password.html', form=form)

@app.route('/password_changed')
def password_changed():
    return "Password changed successfully"

# Note: The actual database operations and password hashing would be implemented
# in a separate function and would need to be properly secured