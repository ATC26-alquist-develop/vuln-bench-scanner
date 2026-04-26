from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return {'error': 'Authentication required'}, 401
    
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)
    
    if not product_id or not quantity:
        return {'error': 'Invalid input'}, 400
    
    try:
        quantity = int(quantity)
        if quantity < 1:
            return {'error': 'Quantity must be positive'}, 400
    except ValueError:
        return {'error': 'Invalid quantity'}, 400
    
    user = User.query.get(session['user_id'])
    if not user:
        return {'error': 'User not found'}, 404
    
    cart_item = CartItem(product_id=product_id, quantity=quantity)
    user.cart_items.append(cart_item)
    db.session.commit()
    
    return {'message': 'Item added to cart'}, 201

@app.route('/cart', methods=['GET'])
def get_cart():
    if 'user_id' not in session:
        return {'error': 'Authentication required'}, 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return {'error': 'User not found'}, 404
    
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    return {'cart_items': [{'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]}, 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)