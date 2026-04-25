from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

class AccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=128)])
    update_email = BooleanField('Update Email')
    update_password = BooleanField('Update Password')

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = AccountForm()
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if form.validate_on_submit():
        user_id = session['user_id']
        if form.update_email.data:
            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", form.email.data):
                form.email.errors.append('Invalid email format')
                return render_template('account.html', form=form)
            
            # Update email in database (implement database logic)
            # ...
            
        if form.update_password.data:
            # Update password in database (implement database logic)
            # ...
            
        return redirect(url_for('account'))
    
    return render_template('account.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)