from flask import Flask, request

# ===== cell separator =====

app = Flask(__name__)

# ===== cell separator =====

@app.route('/', methods=['GET', 'POST'])
   def index():
       return 'Hello, World!'

# ===== cell separator =====

from flask_cors import CORS

   CORS(app)

# ===== cell separator =====

if __name__ == '__main__':
       app.run()