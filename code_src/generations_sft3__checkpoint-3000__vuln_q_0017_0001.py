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
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({'error': 'Invalid quantity'}), 400
            
        if product_id not in session.get('cart', {}).get('items', {}):
            session['cart'] = create_cart()
        
        cart = session['cart']
        item = {
            'product_id': product_id,
            'quantity': quantity,
            'price': Decimal(request.json.get('price'))
        }
        
        cart['items'].append(item)
        cart['total'] += item['price'] * item['quantity']
        
        return jsonify({'message': 'Item added to cart'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/cart', methods=['GET'])
def get_cart():
    try:
        cart = session.get('cart', {})
        return jsonify({
            'items': cart['items'],
            'total': str(cart['total'])
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500