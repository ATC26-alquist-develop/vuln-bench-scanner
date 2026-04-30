from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a secure random secret key

# Database setup
engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)

Base.metadata.create_all(engine)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Input validation
        if not username or not password:
            return "Username and password are required"
        
        # Check if user already exists
        with Session() as session:
            if session.query(User).filter_by(username=username).first():
                return "Username already exists"
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        # Create new user
        with Session() as session:
            new_user = User(username=username, password_hash=password_hash)
            session.add(new_user)
            session.commit()
        
        return redirect(url_for('login'))
    
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <input type="submit" value="Register">
        </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Input validation
        if not username or not password:
            return "Username and password are required"
        
        with Session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                return redirect(url_for('protected'))
            else:
                return "Invalid credentials"
    
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/protected')
def protected():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return "You are logged in"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode in production