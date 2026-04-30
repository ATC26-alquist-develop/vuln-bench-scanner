```python
from typing import List, Dict
from flask import Flask, jsonify
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s'
))
app.logger.addHandler(handler)

# Mock database connection - replace with actual database connection
class MockDatabase:
    @staticmethod
    def get_all_users():
        # This should be replaced with actual database query
        return [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ]

@app.route('/users', methods=['GET'])
def get_users():
    """
    Returns a list of all registered users.
    
    Returns:
        JSON response containing a list of user objects.
    """
    try:
        # Get all users from the database
        users = MockDatabase.get_all_users()
        
        # Log the request for auditing purposes
        app.logger.info(f"GET /users requested by {request.remote_addr}")
        
        # Return the list of users as JSON
        return jsonify({"users": users})
    
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error retrieving users: {str(e)}")
        
        # Return a generic error message to the user
        return jsonify({"error": "An error occurred while retrieving users"}), 500
```