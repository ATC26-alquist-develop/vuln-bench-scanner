from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    content = request.form['content']
    new_message = Message(content=content)
    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:message_id>')
def delete(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)