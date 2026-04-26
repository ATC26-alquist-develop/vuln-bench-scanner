from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionary to store messages
messages = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        messages[name] = message
        return render_template('index.html', messages=messages)
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)