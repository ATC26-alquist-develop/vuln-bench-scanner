from flask import Flask, request, render_template_string
import html

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    messages = []
    if request.method == 'POST':
        # Sanitize user input
        name = html.escape(request.form.get('name', ''))
        message = html.escape(request.form.get('message', ''))
        
        # Validate input
        if not name or not message:
            return render_template_string('''
                <h1>Invalid input</h1>
                <p>Please enter both name and message.</p>
            ''')
        
        # Add sanitized message to list
        messages.append(f"{name}: {message}")
    
    # Render template with messages
    return render_template_string('''
        <h1>Message Board</h1>
        <form method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br>
            <label for="message">Message:</label>
            <textarea id="message" name="message" required></textarea><br>
            <input type="submit" value="Submit">
        </form>
        <h2>Messages:</h2>
        <ul>
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
        </ul>
    ''', messages=messages)

if __name__ == '__main__':
    app.run(debug=False)