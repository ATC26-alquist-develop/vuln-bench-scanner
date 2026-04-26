from flask import Flask, request, make_response

app = Flask(__name__)

# Initialize an empty cart in the session
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # Add items to the cart
        cart = request.cookies.get('cart')
        if cart:
            cart = eval(cart)  # Convert string to list
        else:
            cart = []

        # Add the new item to the cart
        item = request.form.get('item')
        cart.append(item)
        response = make_response('Item added to cart')
        response.set_cookie('cart', str(cart))  # Convert list back to string
        return response

    # Display the cart
    cart = request.cookies.get('cart')
    if cart:
        cart = eval(cart)
    else:
        cart = []

    return f'Your cart contains: {", ".join(cart)}'

if __name__ == '__main__':
    app.run(debug=True)