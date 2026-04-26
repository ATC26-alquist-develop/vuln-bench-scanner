from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import bleach

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)  # Generate secure random key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Guestbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = bleach.clean(request.form.get('message', ''))
        if message:
            new_message = Guestbook(message=message)
            db.session.add(new_message)
            db.session.commit()
        return redirect(url_for('index'))
    
    messages = Guestbook.query.order_by(Guestbook.timestamp.desc()).all()
    return render_template('index.html', messages=messages)

@app.route('/delete/<int:id>')
def delete_message(id):
    message = Guestbook.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)