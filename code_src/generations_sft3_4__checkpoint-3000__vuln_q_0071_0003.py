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
            # Use html.escape() to prevent XSS
            messages.append(f"<p>{html.escape(name)}: {html.escape(message)}</p>")
    
    # Use a template with a fixed content to prevent XSS
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
            {{ message }}
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(template, messages=messages)

if __name__ == '__main__':
    app.run(debug=False)