```python
from flask import Flask, request, escape, render_template_string, abort
import html

app = Flask(__name__)

# Secure storage for messages (in memory for this example)
messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Sanitize and validate input
        name = escape(request.form.get('name', ''))
        message = escape(request.form.get('message', ''))
        
        if name and message and len(message) <= 1000:  # Limit message length
            messages.append({'name': name, 'message': message})
        else:
            abort(400)  # Bad request if validation fails
            
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Secure Message Board</title>
        </head>
        <body>
            <h1>Secure Message Board</h1>
            <form method="POST">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required maxlength="100">
                <br>
                <label for="message">Message:</label>
                <textarea id="message" name="message" required maxlength="1000"></textarea>
                <br>
                <input type="submit" value="Submit">
            </form>
            <h2>Messages:</h2>
            {% for msg in messages %}
                <p><strong>{{ msg.name|e }}</strong>: {{ msg.message|e }}</p>
            {% endfor %}
        </body>
        </html>
    ''', messages=messages)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production
```