from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)

@app.route('/')
def index():
    statuses = Status.query.all()
    return render_template('index.html', statuses=statuses)

@app.route('/post', methods=['POST'])
def post():
    content = request.form['content']
    status = Status(content=content)
    db.session.add(status)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)