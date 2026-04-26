from flask import Flask, request, render_template, redirect, url_for, flash
   from flask_mail import Mail, Message
   from itsdangerous import URLSafeTimedSerializer, SignatureExpired
   from werkzeug.security import generate_password_hash, check_password_hash
   from flask_sqlalchemy import SQLAlchemy

   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'your_secret_key'
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
   app.config['MAIL_SERVER'] = 'smtp.example.com'
   app.config['MAIL_PORT'] = 587
   app.config['MAIL_USE_TLS'] = True
   app.config['MAIL_USERNAME'] = 'your_email@example.com'
   app.config['MAIL_PASSWORD'] = 'your_email_password'
   app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

   db = SQLAlchemy(app)
   mail = Mail(app)

   class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       email = db.Column(db.String(120), unique=True, nullable=False)
       password_hash = db.Column(db.String(128), nullable=False)

       def set_password(self, password):
           self.password_hash = generate_password_hash(password)

       def check_password(self, password):
           return check_password_hash(self.password_hash, password)

   db.create_all()

# ===== cell separator =====

from itsdangerous import URLSafeTimedSerializer

   serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

   @app.route('/reset_password', methods=['GET', 'POST'])
   def reset_password():
       if request.method == 'POST':
           email = request.form['email']
           user = User.query.filter_by(email=email).first()
           if user:
               token = serializer.dumps(email, salt='password-reset-salt')
               reset_url = url_for('reset_with_token', token=token, _external=True)
               msg = Message('Password Reset Request', recipients=[email])
               msg.body = f'Please click the link to reset your password: {reset_url}'
               mail.send(msg)
               flash('A password reset email has been sent. Please check your inbox.', 'info')
               return redirect(url_for('login'))
           else:
               flash('Email not found.', 'error')
       return render_template('reset_password.html')