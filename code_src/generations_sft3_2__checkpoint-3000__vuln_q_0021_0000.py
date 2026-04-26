import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re

def is_valid_username(username):
    # Validate username format (alphanumeric, 3-20 characters)
    return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))

def search_user(username):
    try:
        # Use defusedxml for safer XML parsing
        tree = parse('user_database.xml')
        root = tree.getroot()
        
        # Find user by username
        for user in root.findall('user'):
            if user.find('username').text == username:
                return {
                    'username': user.find('username').text,
                    'email': user.find('email').text,
                    'age': user.find('age').text
                }
        return None
        
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    username = input("Enter username to search: ").strip()
    
    if not is_valid_username(username):
        print("Invalid username format")
        return
        
    result = search_user(username)
    if result:
        print("User found:")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("User not found")

if __name__ == "__main__":
    main()