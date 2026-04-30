from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager
from typing import Dict, Any
import json
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)  # Generate a secure secret key
jwt = JWTManager(app)

# In-memory cart storage (replace with database in production)
carts: Dict[str, Dict[str, Any]] = {}

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        # Validate input
        data = request.get_json()
        if not data or 'item' not in data or 'quantity' not in data:
            return jsonify({"error": "Invalid input"}), 400

        # Sanitize and validate item and quantity
        item = str(data['item']).strip()
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({"error": "Invalid quantity"}), 400

        # Create or update cart for the user
        user_id = secrets.token_urlsafe(8)  # Generate a unique user ID
        if user_id not in carts:
            carts[user_id] = {}

        # Add or update item in cart
        if item in carts[user_id]:
            carts[user_id][item] += quantity
        else:
            carts[user_id][item] = quantity

        # Create JWT payload with cart data
        payload = {
            'user_id': user_id,
            'cart': carts[user_id],
            'exp': datetime.utcnow() + timedelta(hours=24)  # 24-hour expiration
        }

        # Create and sign JWT
        jwt_payload = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        # Create response with JWT
        response = make_response(jsonify({"message": "Item added to cart"}))
        response.set_cookie('shopping_cart', jwt_payload, httponly=True, secure=True, samesite='Strict')
        
        return response

    except Exception as e:
        app.logger.error(f"Error in add_to_cart: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/get_cart', methods=['GET'])
def get_cart():
    try:
        # Retrieve JWT from cookie
        jwt_token = request.cookies.get('shopping_cart')
        if not jwt_token:
            return jsonify({"error": "No cart found"}), 404

        # Verify and decode JWT
        try:
            payload = jwt.decode(jwt_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Cart has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid cart token"}), 401

        # Return cart data
        return jsonify({
            "cart": payload.get('cart', {}),
            "user_id": payload.get('user_id')
        })

    except Exception as e:
        app.logger.error(f"Error in get_cart: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500