import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re

def sanitize_input(user_input):
    """Sanitize user input to prevent XML injection"""
    return re.sub(r'[^\w\s-]', '', user_input)

def search_user(username):
    try:
        # Use defusedxml for secure XML parsing
        tree = parse('user_records.xml')
        root = tree.getroot()
        
        # Use XPath to search for user records
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

if __name__ == "__main__":
    username = input("Enter username to search: ")
    search_user(username)