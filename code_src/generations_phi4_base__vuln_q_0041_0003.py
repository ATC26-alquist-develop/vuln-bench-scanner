from flask import Flask, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Add other fields as necessary

# Create the database tables
with app.app_context():
    db.create_all()

# ===== cell separator =====

@app.route('/delete_account/<int:user_id>', methods=['POST'])
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('index'))

# ===== cell separator =====

if __name__ == '__main__':
    app.run(debug=True)