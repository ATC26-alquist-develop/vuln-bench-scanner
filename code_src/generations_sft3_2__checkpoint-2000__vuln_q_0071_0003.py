from flask import Flask, request, render_template_string, escape
import html

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    messages = []
    if request.method == 'POST':
        # Sanitize user input
        name = escape(request.form.get('name', ''))
        message = escape(request.form.get('message', ''))
        
        # Validate input
        if name and message:
            # Convert message to HTML-safe string
            safe_message = html.escape(message)
            messages.append(f"<p>{name}: {safe_message}</p>")
    
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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