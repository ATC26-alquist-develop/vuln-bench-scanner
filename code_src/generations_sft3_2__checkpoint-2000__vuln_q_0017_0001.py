from flask import Flask, request, session, jsonify
from decimal import Decimal
from typing import Dict, List
import secrets

app = Flask(__name__)

# Generate a secure random secret key
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

def create_cart() -> Dict[str, Decimal]:
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']

def add_to_cart(product_id: int, quantity: int) -> None:
    cart = create_cart()
    if product_id not in cart:
        cart[product_id] = Decimal('0')
    cart[product_id] += Decimal(str(quantity))

def remove_from_cart(product_id: int) -> None:
    cart = create_cart()
    cart.pop(product_id, None)

def get_cart_items() -> List[Dict[str, str]]:
    cart = create_cart()
    return [
        {
            'id': str(product_id),
            'quantity': str(quantity)
        }
        for product_id, quantity in cart.items()
    ]

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart_route():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    
    if not product_id or not quantity:
        return jsonify({'error': 'Missing product_id or quantity'}), 400
    
    try:
        quantity = int(quantity)
        if quantity < 1:
            return jsonify({'error': 'Quantity must be positive'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    add_to_cart(product_id, quantity)
    return jsonify({'message': 'Product added to cart'}), 200

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart_route():
    product_id = request.json.get('product_id')
    
    if not product_id:
        return jsonify({'error': 'Missing product_id'}), 400
    
    remove_from_cart(product_id)
    return jsonify({'message': 'Product removed from cart'}), 200

@app.route('/cart', methods=['GET'])
def get_cart_route():
    return jsonify(get_cart_items()), 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development