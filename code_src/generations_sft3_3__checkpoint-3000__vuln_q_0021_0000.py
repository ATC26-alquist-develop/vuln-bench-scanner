import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re

def is_valid_username(username):
    # Validate username format (alphanumeric, 3-20 characters)
    return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))

def search_user(username):
    try:
        # Validate input
        if not is_valid_username(username):
            return "Invalid username format. Use 3-20 alphanumeric characters only."
        
        # Load XML file using defusedxml (prevents XXE attacks)
        tree = parse("user_database.xml")
        root = tree.getroot()
        
        # Search for user
        for user in root.findall('user'):
            if user.find('username').text == username:
                return {
                    'username': user.find('username').text,
                    'email': user.find('email').text,
                    'age': user.find('age').text
                }
        return "User not found."
    
    except ET.ParseError:
        return "Error: Invalid XML file format."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main program
if __name__ == "__main__":
    username = input("Enter username to search: ")
    result = search_user(username)
    print(result)