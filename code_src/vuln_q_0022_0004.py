from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate secure random secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # Session timeout in seconds

# Simulated database (replace with actual database in production)
users = {}

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=128)])
    update_email = BooleanField('Update Email')
    submit = SubmitField('Update Account')

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = AccountForm()
    if 'username' in session:
        user = users.get(session['username'])
        if user:
            form.email.data = user['email']
            form.update_email.data = user['update_email']
    return render_template('account.html', form=form)

@app.route('/account', methods=['POST'])
def update_account():
    form = AccountForm(request.form)
    if form.validate():
        username = request.form['username']
        if username not in users:
            return redirect(url_for('account'))
        
        user = users[username]
        if form.update_email.data:
            user['email'] = form.email.data
            user['update_email'] = False
        
        if form.password.data:
            user['password'] = generate_password_hash(form.password.data)
        
        users[username] = user
        session['username'] = username
        return redirect(url_for('account'))
    
    return render_template('account.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('account'))

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False in production