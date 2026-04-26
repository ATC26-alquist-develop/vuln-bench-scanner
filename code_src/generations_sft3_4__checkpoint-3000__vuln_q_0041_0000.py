import hashlib
import secrets
from flask import Flask, request, session, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400
        
        try:
            user = User(username=username, password_hash=hash_password(password))
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        except IntegrityError:
            return "Username already exists", 400
    
    return render_template_string('''
        <form method="post">
            <input type="text" name="username" required>
            <input type="password" name="password" required>
            <input type="submit" value="Register">
        </form>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400
        
        user = User.query.filter_by(username=username).first()
        if user and user.password_hash == hash_password(password):
            session['user_id'] = user.id
            return redirect('/dashboard')
        
        return "Invalid credentials", 401
    
    return render_template_string('''
        <form method="post">
            <input type="text" name="username" required>
            <input type="password" name="password" required>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return f"Welcome to your dashboard, {session['user_id']}"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(ssl_context='adhoc')  # Enable HTTPS