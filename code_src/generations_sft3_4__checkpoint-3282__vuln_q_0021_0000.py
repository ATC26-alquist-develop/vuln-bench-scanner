from lxml import etree
import sys
import os

def search_user(username):
    # Validate input
    if not isinstance(username, str) or len(username) == 0:
        raise ValueError("Invalid username format")
    
    # Sanitize input by removing potentially dangerous characters
    username = ''.join(c for c in username if c.isalnum() or c in ('-', '_'))
    
    # Define safe file path
    xml_file = os.path.join(os.getcwd(), 'users.xml')
    
    try:
        # Parse XML safely
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        # Search for user
        for user in root.findall('.//user'):
            if user.find('username').text == username:
                return {
                    'username': user.find('username').text,
                    'email': user.find('email').text,
                    'age': user.find('age').text
                }
        return None
        
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    try:
        username = input("Enter username to search: ")
        result = search_user(username)
        if result:
            print("User found:")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print("User not found")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()