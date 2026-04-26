from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        token = s.dumps(email, salt='password-reset-salt')
        msg = Message('Password Reset Request', sender='your-email@gmail.com', recipients=[email])
        link = url_for('reset_with_token', token=token, _external=True)
        msg.body = 'Your link to reset your password is: {}'.format(link)
        mail.send(msg)
        return 'A password reset link has been sent to your email address.'
    return render_template('reset_password.html')

@app.route('/reset_with_token/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        return 'The password reset link has expired. Please try again.'
    if request.method == 'POST':
        new_password = request.form['password']
        # Update the user's password in the database
        return redirect(url_for('login'))
    return render_template('reset_with_token.html', token=token)

if __name__ == '__main__':
    app.run()