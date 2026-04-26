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
        
        # Use XPath to find user records
        xpath_query = f"//user[@username='{sanitize_input(username)}']"
        user_elements = root.findall(xpath_query)
        
        if user_elements:
            for user in user_elements:
                print(f"Username: {user.find('username').text}")
                print(f"Email: {user.find('email').text}")
                print("---")
        else:
            print("User not found.")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        username = input("Enter username to search (or 'quit' to exit): ")
        if username.lower() == 'quit':
            break
        search_user(username)

if __name__ == "__main__":
    main()