from defusedxml import ElementTree as ET
import re
from pathlib import Path

def sanitize_input(user_input):
    # Remove any potentially dangerous characters
    return re.sub(r'[^\w\s-]', '', user_input)

def search_user(username):
    try:
        # Use pathlib for safer file handling
        xml_file = Path("user_records.xml")
        
        # Validate file exists and is a file
        if not xml_file.is_file():
            return "XML file not found"
            
        # Parse XML safely
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Search for user
        for user in root.findall(".//user"):
            if user.find("username").text == username:
                return {
                    "username": user.find("username").text,
                    "email": user.find("email").text,
                    "age": user.find("age").text
                }
        return "User not found"
        
    except ET.ParseError:
        return "Invalid XML file"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    username = input("Enter username to search: ")
    result = search_user(sanitize_input(username))
    print(result)