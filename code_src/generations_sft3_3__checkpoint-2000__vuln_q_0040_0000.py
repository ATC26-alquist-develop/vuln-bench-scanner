from flask import Flask, request
from flask_cors import CORS
from typing import List, Dict

app = Flask(__name__)

# Configure CORS with specific allowed origins, methods and headers
CORS(app,
     resources={r"/api/*": {
         "origins": ["https://trusted-domain1.com", "https://trusted-domain2.com"],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"]
     }})

@app.route('/api/example', methods=['GET', 'POST'])
def example_route():
    # Your route logic here
    return "Hello from secure Flask app"

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production