from defusedxml import ElementTree as ET
from defusedxml.ElementTree import ParseError
import re

def search_user(xml_file, username):
    try:
        # Validate XML file path
        if not xml_file or not isinstance(xml_file, str):
            raise ValueError("Invalid XML file path")

        # Validate username input
        if not username or not isinstance(username, str):
            raise ValueError("Invalid username")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError("Invalid username format")

        # Parse XML safely
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define XPath query
        xpath_query = f"//user[username='{username}']"

        # Find matching user
        user = root.find(xpath_query)

        if user is not None:
            return {
                'username': user.find('username').text,
                'email': user.find('email').text,
                'age': user.find('age').text
            }
        else:
            return None

    except (ParseError, ValueError) as e:
        return {'error': str(e)}

# Example usage
xml_file = 'users.xml'
username = input("Enter username: ")
result = search_user(xml_file, username)

if result:
    print("User found:", result)
else:
    print("User not found or error:", result.get('error', 'Unknown error'))