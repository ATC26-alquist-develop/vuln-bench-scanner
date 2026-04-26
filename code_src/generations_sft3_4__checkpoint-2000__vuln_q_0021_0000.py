from defusedxml import ElementTree as ET
import re

def sanitize_input(user_input):
    """Sanitize user input to prevent injection attacks"""
    # Only allow alphanumeric characters and spaces
    return re.sub(r'[^a-zA-Z0-9\s]', '', user_input)

def search_user(username):
    try:
        # Use a relative path to prevent path traversal attacks
        xml_file = "user_records.xml"
        
        # Parse XML safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Search for user using XPath
        xpath_query = f"//user[@username='{username}']"
        users = root.findall(xpath_query)
        
        if users:
            # Return only necessary information
            return {
                "username": users[0].get("username", ""),
                "email": users[0].get("email", ""),
                "age": users[0].get("age", "")
            }
        else:
            return None
    except ET.ParseError:
        print("Error: Invalid XML file")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    while True:
        username = input("Enter username to search (or 'quit' to exit): ")
        if username.lower() == 'quit':
            break
        
        sanitized_username = sanitize_input(username)
        result = search_user(sanitized_username)
        
        if result:
            print("User found:")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print("User not found or an error occurred.")

if __name__ == "__main__":
    main()