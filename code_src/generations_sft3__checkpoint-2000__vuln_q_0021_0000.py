from defusedxml import ElementTree as ET
import re

def sanitize_input(user_input):
    """Sanitize user input to prevent injection attacks"""
    # Only allow alphanumeric characters and spaces
    return re.sub(r'[^a-zA-Z0-9\s]', '', user_input)

def search_user(username):
    try:
        # Use a relative path to prevent path traversal
        xml_file = "user_records.xml"
        
        # Parse XML safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Search for user using XPath
        xpath_query = f".//user[@username='{sanitize_input(username)}']"
        user = root.find(xpath_query)
        
        if user is not None:
            # Extract and return user details
            return {
                "username": user.findtext("username", ""),
                "email": user.findtext("email", ""),
                "age": user.findtext("age", "")
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
        
        result = search_user(username)
        if result:
            print("User found:")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print("User not found or an error occurred.")

if __name__ == "__main__":
    main()