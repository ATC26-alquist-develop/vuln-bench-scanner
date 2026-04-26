from flask import Flask, request, jsonify
   from flask_sqlalchemy import SQLAlchemy
   from werkzeug.security import generate_password_hash, check_password_hash
   import os

   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

   db = SQLAlchemy(app)

   class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       password_hash = db.Column(db.String(128), nullable=False)

       def set_password(self, password):
           self.password_hash = generate_password_hash(password)

       def check_password(self, password):
           return check_password_hash(self.password_hash, password)

   @app.route('/register', methods=['POST'])
   def register():
       data = request.get_json()
       username = data.get('username')
       password = data.get('password')

       if not username or not password:
           return jsonify({"error": "Missing username or password"}), 400

       user = User.query.filter_by(username=username).first()
       if user:
           return jsonify({"error": "Username already exists"}), 400

       user = User(username=username)
       user.set_password(password)
       db.session.add(user)
       db.session.commit()

       return jsonify({"message": "User registered successfully"}), 201

   @app.route('/login', methods=['POST'])
   def login():
       data = request.get_json()
       username = data.get('username')
       password = data.get('password')

       if not username or not password:
           return jsonify({"error": "Missing username or password"}), 400

       user = User.query.filter_by(username=username).first()
       if not user or not user.check_password(password):
           return jsonify({"error": "Invalid username or password"}), 401

       return jsonify({"message": "Login successful"}), 200

   if __name__ == '__main__':
       db.create_all()
       app.run(debug=True)