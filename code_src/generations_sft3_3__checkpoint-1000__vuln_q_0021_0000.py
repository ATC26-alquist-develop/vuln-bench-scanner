import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re

def sanitize_input(user_input):
    """Sanitize user input to prevent XML injection"""
    return re.sub(r'[^\w\s-]', '', user_input)

def search_user(username):
    """Search for user records using XPath"""
    try:
        # Use defusedxml to safely parse XML
        tree = parse('user_records.xml')
        root = tree.getroot()
        
        # Sanitize user input
        safe_username = sanitize_input(username)
        
        # Use XPath to search for user records
        xpath_query = f".//user[@username='{safe_username}']"
        users = root.findall(xpath_query)
        
        if users:
            return [user.text for user in users]
        else:
            return "User not found"
    
    except ET.ParseError:
        return "Error: Invalid XML file"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    while True:
        username = input("Enter username to search (or 'quit' to exit): ")
        if username.lower() == 'quit':
            break
        
        result = search_user(username)
        print(result)

if __name__ == "__main__":
    main()