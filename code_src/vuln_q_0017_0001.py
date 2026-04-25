from flask import Flask, session, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a secure random secret key

# Simulated database of items (in a real app, use a proper database)
items_db = {
    'item1': {'name': 'Product 1', 'price': 10.99},
    'item2': {'name': 'Product 2', 'price': 19.99},
    'item3': {'name': 'Product 3', 'price': 5.99}
}

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    item_id = request.json.get('item_id')
    if not item_id or item_id not in items_db:
        return jsonify({'error': 'Invalid item ID'}), 400
    
    session['cart'].append(item_id)
    return jsonify({'message': 'Item added to cart', 'cart': session['cart']}), 200

@app.route('/get_cart', methods=['GET'])
def get_cart():
    cart = session.get('cart', [])
    cart_items = [items_db[item_id] for item_id in cart]
    return jsonify({'cart': cart_items}), 200

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return jsonify({'message': 'Cart cleared'}), 200

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production