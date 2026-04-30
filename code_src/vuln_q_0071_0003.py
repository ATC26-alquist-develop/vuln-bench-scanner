```python
from flask import Flask, request, render_template_string, redirect, url_for
import html

app = Flask(__name__)

# In-memory storage for messages
messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get name and message from form
        name = request.form.get('name')
        message = request.form.get('message')
        
        # Validate input
        if name and message:
            # Sanitize inputs to prevent XSS
            name = html.escape(name)
            message = html.escape(message)
            
            # Store sanitized message
            messages.append({'name': name, 'message': message})
        
        # Redirect to prevent form resubmission
        return redirect(url_for('index'))
    
    # Render the form and messages
    return render_template_string('''
        <html>
            <head>
                <title>Message Board</title>
            </head>
            <body>
                <h1>Enter Your Message</h1>
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
                <ul>
                    {% for msg in messages %}
                    <li><strong>{{ msg.name }}:</strong> {{ msg.message }}</li>
                    {% endfor %}
                </ul>
            </body>
        </html>
    ''', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
```