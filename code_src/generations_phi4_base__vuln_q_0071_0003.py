from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for messages
messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        messages.append({'name': name, 'message': message})
        return redirect(url_for('index'))
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)