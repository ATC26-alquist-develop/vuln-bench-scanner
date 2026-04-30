from flask import Flask, request, render_template, escape
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import bleach

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

@app.route('/comment', methods=['POST'])
def post_comment():
    post_id = request.form.get('post_id')
    user_id = request.form.get('user_id')
    content = request.form.get('content')
    
    if not post_id or not user_id or not content:
        return "Invalid input", 400
    
    sanitized_content = bleach.clean(content, tags=['p', 'br', 'strong', 'em'], strip=True)
    
    new_comment = Comment(post_id=post_id, user_id=user_id, content=sanitized_content)
    db.session.add(new_comment)
    db.session.commit()
    
    return "Comment posted successfully", 201

@app.route('/comments/<int:post_id>')
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('comments.html', comments=comments)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)