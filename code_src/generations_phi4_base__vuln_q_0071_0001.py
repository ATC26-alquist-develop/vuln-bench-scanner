from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for messages
messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['GET', 'POST'])
def post_message():
    if request.method == 'POST':
        message = request.form['message']
        messages.append(message)
        return redirect(url_for('index'))
    return render_template('post.html')

if __name__ == '__main__':
    app.run(debug=True)