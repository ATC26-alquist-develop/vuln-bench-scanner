from flask import Flask, request, redirect, url_for
import uuid
import os

app = Flask(__name__)

# Directory to store the mappings between short and long URLs
short_url_dir = 'short_urls'

# Ensure the directory exists
if not os.path.exists(short_url_dir):
    os.makedirs(short_url_dir)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_id = str(uuid.uuid4())[:8]  # Generate a short ID
    short_url = f"/{short_id}"

    # Save the mapping in a file
    with open(os.path.join(short_url_dir, short_id), 'w') as f:
        f.write(long_url)

    return redirect(short_url)

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    # Load the long URL from the file
    long_url = None
    for file in os.listdir(short_url_dir):
        if file.startswith(short_id):
            with open(os.path.join(short_url_dir, file), 'r') as f:
                long_url = f.read().strip()
            break

    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)