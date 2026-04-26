from flask import Flask, session, request, jsonify
from decimal import Decimal
from typing import Dict, List

app = Flask(__name__)

# Use strong, randomly generated secret key
app.secret_key = 'your-very-long-secret-key-here'

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
        
        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return jsonify({'error': 'Invalid quantity'}), 400
        
        # Get cart from session or create new
        cart = session.get('cart')
        if not cart:
            cart = create_cart()
            session['cart'] = cart
        
        # Add item to cart
        item = {
            'product_id': product_id,
            'quantity': quantity,
            'price': Decimal('10.00')  # This should be retrieved from database
        }
        cart['items'].append(item)
        cart['total'] += item['price'] * item['quantity']
        
        return jsonify({'message': 'Item added to cart'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/cart', methods=['GET'])
def get_cart():
    cart = session.get('cart')
    if not cart:
        return jsonify({'items': [], 'total': Decimal('0.00')})
    
    # Convert Decimal to float for JSON serialization
    cart['total'] = float(cart['total'])
    return jsonify(cart), 200