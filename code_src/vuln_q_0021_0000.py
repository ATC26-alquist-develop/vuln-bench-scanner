from defusedxml.ElementTree import fromstring, parse
import re

def search_user(xml_file, username):
    # Validate username input
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValueError("Invalid username format")

    try:
        # Parse XML safely
        tree = parse(xml_file)
        root = tree.getroot()

        # Find user with matching username
        user = root.find(f".//user[@username='{username}']")
        if user is None:
            return None

        # Extract and return user details
        return {
            'id': user.get('id'),
            'name': user.find('name').text,
            'email': user.find('email').text
        }
    except Exception as e:
        print(f"Error processing XML: {e}")
        return None

# Usage example
xml_file = 'users.xml'
username = input("Enter username: ")
user_details = search_user(xml_file, username)

if user_details:
    print("User found:", user_details)
else:
    print("User not found or error occurred.")