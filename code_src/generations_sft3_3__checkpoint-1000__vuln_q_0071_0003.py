from flask import Flask, request, render_template_string
import html

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    messages = []
    if request.method == 'POST':
        name = request.form.get('name', '')
        message = request.form.get('message', '')
        
        # Sanitize inputs to prevent XSS
        name = html.escape(name)
        message = html.escape(message)
        
        # Store sanitized data
        messages.append(f"{name}: {message}")
    
    # Use a simple template to display messages
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Message Board</title>
    </head>
    <body>
        <h1>Message Board</h1>
        <form method="POST">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br><br>
            <label for="message">Message:</label>
            <textarea id="message" name="message" required></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
        <h2>Messages:</h2>
        <ul>
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    '''
    
    return render_template_string(template, messages=messages)

if __name__ == '__main__':
    app.run(debug=False)