# Simulated product database
products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
    {"id": 2, "name": "Smartphone", "price": 699.99, "category": "Electronics"},
    {"id": 3, "name": "Coffee Maker", "price": 89.99, "category": "Home Appliances"},
    {"id": 4, "name": "Blender", "price": 49.99, "category": "Home Appliances"},
    {"id": 5, "name": "Headphones", "price": 199.99, "category": "Electronics"},
]

def search_products(product_name):
    # Search for products by name
    results = [product for product in products if product_name.lower() in product["name"].lower()]
    
    if results:
        print("Search results:")
        for product in results:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: ${product['price']:.2f}, Category: {product['category']}")
    else:
        print("No products found with that name.")

def main():
    while True:
        product_name = input("Enter a product name to search (or type 'exit' to quit): ")
        if product_name.lower() == 'exit':
            print("Exiting the search.")
            break
        search_products(product_name)

if __name__ == "__main__":
    main()