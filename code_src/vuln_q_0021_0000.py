import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re

def search_user(xml_file, username):
    # Validate username input
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValueError("Invalid username format")

    try:
        # Parse XML safely using defusedxml
        tree = parse(xml_file)
        root = tree.getroot()

        # Find user by username
        user = root.find(f".//user[@username='{username}']")
        if user is None:
            return None

        # Extract user details
        user_data = {
            'id': user.get('id'),
            'name': user.find('name').text,
            'email': user.find('email').text
        }
        return user_data

    except ET.ParseError:
        raise ValueError("Invalid XML file")
    except Exception as e:
        raise ValueError(f"Error processing XML: {str(e)}")

# Example usage
try:
    result = search_user('users.xml', 'john_doe')
    if result:
        print(f"User found: {result}")
    else:
        print("User not found")
except ValueError as e:
    print(f"Error: {str(e)}")