from flask import Flask, session, request, jsonify
from decimal import Decimal
from typing import Dict, List
import secrets

app = Flask(__name__)

# Generate a secure secret key
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
    try:
        product_id = request.json.get('product_id')
        quantity = request.json.get('quantity')
        
        if not product_id or not quantity:
            return jsonify({'error': 'Missing product_id or quantity'}), 400
        
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({'error': 'Invalid quantity'}), 400
        
        if product_id not in session.get('cart', {}).get('items', {}):
            session['cart']['items'].append(product_id)
        
        session['cart']['total'] += Decimal(str(quantity)) * Decimal('1.00')
        
        return jsonify({'message': 'Product added to cart'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    try:
        product_id = request.json.get('product_id')
        
        if not product_id:
            return jsonify({'error': 'Missing product_id'}), 400
        
        if product_id in session.get('cart', {}).get('items', []):
            session['cart']['items'].remove(product_id)
            session['cart']['total'] -= Decimal('1.00')
        
        return jsonify({'message': 'Product removed from cart'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get_cart', methods=['GET'])
def get_cart():
    try:
        cart = session.get('cart', {})
        return jsonify(cart), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500