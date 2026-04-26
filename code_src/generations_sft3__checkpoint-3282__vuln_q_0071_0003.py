from flask import Flask, request, render_template_string, escape
import html

app = Flask(__name__)

# Store submitted messages in a list
messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get and sanitize user input
        name = escape(request.form.get('name', '').strip())
        message = escape(request.form.get('message', '').strip())
        
        # Sanitize HTML content
        message = html.escape(message)
        
        # Store sanitized message
        messages.append(f"<p>{name}: {message}</p>")
    
    # Render template with messages
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Message Board</title>
    </head>
    <body>
        <h1>Message Board</h1>
        <form method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br><br>
            <label for="message">Message:</label>
            <textarea id="message" name="message" required></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
        {% for message in messages %}
            {{ message|safe }}
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(template, messages=messages)

if __name__ == '__main__':
    app.run(debug=False)