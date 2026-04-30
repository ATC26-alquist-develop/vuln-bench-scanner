```python
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
```


This implementation includes several security measures:

1. Input sanitization: We use the `bleach` library to sanitize user input, preventing XSS attacks.
2. Parameterized queries: SQLAlchemy ORM is used, which helps prevent SQL injection attacks.
3. Password hashing: Although not directly used in this example, the User model includes a password_hash field for secure password storage.
4. CSRF protection: Flask-WTF's CSRF protection is recommended for forms (not shown in this example).
5. Content Security Policy: Implement CSP headers in production to prevent XSS.
6. Debug mode disabled: The app runs with debug=False to prevent information leakage in production.
7. Input validation: Basic checks are performed to ensure required fields are not empty.
8. Secure database configuration: Using SQLite with SQLAlchemy ORM helps prevent direct database access.

Note that this is a basic implementation and additional security measures should be implemented in a production environment, such as rate limiting, authentication, and proper error handling. Always keep dependencies updated and follow the latest security best practices.