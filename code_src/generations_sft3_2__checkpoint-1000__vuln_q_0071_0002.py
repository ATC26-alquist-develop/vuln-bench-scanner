from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import bleach
import re
from datetime import datetime
from flask_login import login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/comment', methods=['POST'])
@login_required
def add_comment():
    content = bleach.clean(request.form.get('content', ''))
    if not content:
        return "Comment cannot be empty", 400
    
    # Validate content length
    if len(content) > 500:
        return "Comment length exceeds limit", 400
    
    # Validate content for XSS
    if re.search(r'<script.*?>.*?</script>', content, re.IGNORECASE):
        return "Invalid content", 400
    
    new_comment = Comment(
        content=content,
        author=current_user.username
    )
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/moderate')
@login_required
def moderate_comments():
    comments = Comment.query.filter_by(approved=False).all()
    return render_template('moderate.html', comments=comments)

@app.route('/approve/<int:comment_id>')
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.approved = True
    db.session.commit()
    return redirect(url_for('moderate_comments'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)