from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    settings = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Account {self.username}>'

@app.route('/update_account_settings', methods=['POST'])
def update_account_settings():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'settings' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    username = data['username']
    email = data['email']
    settings = data['settings']

    # Fetch the account
    account = Account.query.filter_by(username=username).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Update the account settings
    account.settings = settings
    db.session.commit()

    return jsonify({"message": "Account settings updated successfully", "account": account}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)