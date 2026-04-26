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
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

db = SQLAlchemy(app)

class Guestbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = bleach.clean(request.form.get('name', ''))
        message = bleach.clean(request.form.get('message', ''))
        
        if name and message:
            guestbook = Guestbook(name=name, message=message)
            db.session.add(guestbook)
            db.session.commit()
        return redirect(url_for('index'))
    
    entries = Guestbook.query.order_by(Guestbook.timestamp.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/delete/<int:id>')
def delete_entry(id):
    entry = Guestbook.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)