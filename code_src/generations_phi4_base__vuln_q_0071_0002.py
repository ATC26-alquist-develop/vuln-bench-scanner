from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for comments
comments = []

@app.route('/')
def index():
    return render_template('index.html', comments=comments)

@app.route('/post_comment', methods=['POST'])
def post_comment():
    name = request.form.get('name')
    comment = request.form.get('comment')
    if name and comment:
        comments.append({'name': name, 'comment': comment})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)