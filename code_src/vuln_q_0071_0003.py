from flask import Flask, request, render_template_string, escape
import html

app = Flask(__name__)

# Secure template with CSRF protection
TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Message Board</title>
  </head>
  <body>
    <h1>Message Board</h1>
    <form method="post">
      <label for="name">Name:</label>
      <input type="text" id="name" name="name" required>
      <br>
      <label for="message">Message:</label>
      <textarea id="message" name="message" required></textarea>
      <br>
      <input type="submit" value="Submit">
    </form>
    <h2>Messages:</h2>
    {% for name, message in messages %}
      <p><strong>{{ name|e }}</strong>: {{ message|e }}</p>
    {% endfor %}
  </body>
</html>
"""

messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '')
        message = request.form.get('message', '')
        if name and message:
            messages.append((name, message))
    return render_template_string(TEMPLATE, messages=messages)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')