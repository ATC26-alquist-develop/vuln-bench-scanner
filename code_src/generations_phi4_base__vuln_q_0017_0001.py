from http.cookies import SimpleCookie

def store_cart_items_in_cookies(cart_items):
    cookie = SimpleCookie()
    cookie['cart'] = '; '.join([f"{item['id']}={item['quantity']}" for item in cart_items])
    cookie['cart']['path'] = '/'
    cookie['cart']['max-age'] = 3600  # Set the expiration time for the cookie (in seconds)
    return cookie.output(header='', sep='')

# Example usage
cart_items = [
    {'id': 'item1', 'quantity': '2'},
    {'id': 'item2', 'quantity': '1'}
]

cookie_string = store_cart_items_in_cookies(cart_items)
print(cookie_string)