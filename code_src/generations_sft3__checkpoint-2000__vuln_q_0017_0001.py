from flask import Flask, session, request, jsonify
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
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# In-memory cart storage for demonstration
# In production, use a secure database
cart: Dict[str, Dict[str, Decimal]] = {}

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)
    
    # Validate inputs
    if not product_id or not quantity:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return jsonify({'error': 'Invalid quantity'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity format'}), 400
    
    if product_id not in cart:
        cart[product_id] = {}
    
    cart[product_id]['quantity'] = quantity
    
    return jsonify({'message': 'Product added to cart'}), 200

@app.route('/cart', methods=['GET'])
def get_cart():
    # Only authenticated users can access the cart
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Create a copy of cart to prevent modifications
    cart_items = cart.copy()
    
    # Remove any products not in the current session
    for product_id in list(cart_items.keys()):
        if product_id not in session.get('cart_items', []):
            del cart_items[product_id]
    
    return jsonify(cart_items), 200

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    
    if not product_id:
        return jsonify({'error': 'Missing product_id'}), 400
    
    if product_id in cart:
        del cart[product_id]
    
    return jsonify({'message': 'Product removed from cart'}), 200