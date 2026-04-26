from flask import Flask, session, request, jsonify
from decimal import Decimal
from typing import Dict, List
import secrets

app = Flask(__name__)

# Generate secure random secret key
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

def create_cart() -> Dict:
    return {
        'items': [],
        'total': Decimal('0.00')
    }

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)
    
    # Validate input
    if not product_id or not quantity:
        return jsonify({'error': 'Invalid input'}), 400
    
    try:
        quantity = int(quantity)
        if quantity < 1:
            return jsonify({'error': 'Quantity must be positive'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    # Get or create cart
    if 'cart' not in session:
        session['cart'] = create_cart()
    
    cart = session['cart']
    product = {'id': product_id, 'quantity': quantity}
    
    # Check if product exists in cart
    if product['id'] in [item['id'] for item in cart['items']]:
        cart['items'] = [
            item for item in cart['items']
            if item['id'] != product['id']
        ]
        cart['items'].append(product)
    else:
        cart['items'].append(product)
    
    cart['total'] = Decimal(str(cart['total'])) + Decimal(str(product['quantity'] * 1.00))
    cart['total'] = max(cart['total'], Decimal('0.00'))
    
    return jsonify({'message': 'Product added to cart', 'cart': cart}), 200

@app.route('/cart', methods=['GET'])
def get_cart():
    cart = session.get('cart', create_cart())
    return jsonify({'cart': cart}), 200

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    
    if not product_id:
        return jsonify({'error': 'Invalid input'}), 400
    
    # Get or create cart
    if 'cart' not in session:
        return jsonify({'message': 'Cart is empty'}), 200
    
    cart = session['cart']
    cart['items'] = [item for item in cart['items'] if item['id'] != product_id]
    cart['total'] = Decimal(str(cart['total'])) - Decimal('1.00')
    cart['total'] = max(cart['total'], Decimal('0.00'))
    
    return jsonify({'message': 'Product removed from cart', 'cart': cart}), 200