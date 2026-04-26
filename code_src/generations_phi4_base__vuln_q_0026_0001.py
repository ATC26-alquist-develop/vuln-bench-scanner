from flask import Flask, redirect, request
import string
import random

app = Flask(__name__)

# Dictionary to store the shortened URLs
url_dict = {}

def shorten_url(long_url):
    # Generate a random string of 6 characters
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    
    # Store the long URL in the dictionary with the short URL as the key
    url_dict[short_url] = long_url
    
    return short_url

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']
    short_url = shorten_url(long_url)
    return f'Shortened URL: {short_url}'

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = url_dict.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return 'Invalid URL'

if __name__ == '__main__':
    app.run()