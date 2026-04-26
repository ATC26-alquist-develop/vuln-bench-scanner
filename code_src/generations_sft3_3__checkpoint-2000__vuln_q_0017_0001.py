I'll help you implement a secure shopping cart feature. Storing cart items in cookies is not recommended for e-commerce due to security concerns. Instead, I'll show you how to implement a more secure approach using server-side storage with sessions. Here's a safe implementation:

```python
from flask import Flask, session, request, jsonify
from decimal import Decimal
from typing import Dict, List
import secrets

app = Flask(__name__)

# Generate a secure random secret key
app.secret_key = secrets.token_hex(32)

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
        
        # Get or create cart
        if 'cart' not in session:
            session['cart'] = create_cart()
        
        cart = session['cart']
        
        # Check if product exists in cart
        if product_id in [item['id'] for item in cart['items']]:
            for item in cart['items']:
                if item['id'] == product_id:
                    item['quantity'] += quantity
                    break
        else:
            cart['items'].append({
                'id': product_id,
                'quantity': quantity,
                'price': Decimal('0.00')  # Will be set later
            })
        
        # Calculate total
        cart['total'] = sum(
            item['price'] * item['quantity']
            for item in cart['items']
        )
        
        return jsonify({'message': 'Product added to cart'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/update_cart', methods=['POST'])
def update_cart():
    try:
        product_id = request.json.get('product_id')
        quantity = request.json.get('quantity')
        
        if not product_id or not quantity:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError
        except ValueError:
            return jsonify({'error': 'Invalid quantity'}), 400
        
        # Get cart
        cart = session.get('cart')
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404
        
        # Update item quantity
        for item in cart['items']:
            if item['id'] == product_id:
                item['quantity'] = quantity
                break
        
        # Recalculate total
        cart['total'] = sum(
            item['price'] * item['quantity']
            for item in cart['items']
        )
        
        return jsonify({'message': 'Cart updated'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    try:
        product_id = request.json.get('product_id')
        
        if not product_id:
            return jsonify({'error': 'Missing product_id'}), 400
        
        # Get cart
        cart = session.get('cart')
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404
        
        #