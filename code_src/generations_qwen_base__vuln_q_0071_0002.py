from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data to store comments
comments = []

@app.route('/')
def index():
    return render_template('index.html', comments=comments)

@app.route('/submit', methods=['POST'])
def submit():
    comment = request.form['comment']
    comments.append(comment)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)