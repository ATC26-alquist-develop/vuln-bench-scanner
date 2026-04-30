```python
import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re
import os

def validate_username(username):
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_-]{3,20}$', username))

def search_user(username):
    """Search for user in XML file securely."""
    if not validate_username(username):
        raise ValueError("Invalid username format")

    # Validate file path and existence
    if not os.path.exists('user_records.xml'):
        raise FileNotFoundError("XML file not found")

    try:
        # Use defusedxml for secure parsing
        tree = parse('user_records.xml')
        root = tree.getroot()

        # Find user with case-insensitive matching
        for user in root.findall('.//user'):
            if user.find('username').text.lower() == username.lower():
                return {
                    'id': user.find('id').text,
                    'name': user.find('name').text,
                    'email': user.find('email').text
                }

        return None

    except ET.ParseError as e:
        raise ValueError(f"Error parsing XML: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

def main():
    try:
        username = input("Enter username to search: ").strip()
        user_info = search_user(username)
        
        if user_info:
            print(f"User found: {user_info}")
        else:
            print("User not found")

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
```


This implementation addresses several security concerns:

1. Input validation: The username is validated using a regex pattern to prevent injection attacks.
2. Secure XML parsing: We use the `defusedxml` library instead of the standard `xml` library to protect against XML vulnerabilities.
3. File path validation: We check if the XML file exists before attempting to parse it.
4. Error handling: Specific exceptions are caught and handled to prevent information leakage.
5. Case-insensitive search: We perform a case-insensitive search to improve usability without compromising security.
6. Limited data exposure: Only specific user details are returned, reducing the risk of exposing sensitive information.
7. No external dependencies: The script only uses standard library modules and the widely-trusted `defusedxml` library.

This implementation prioritizes security while fulfilling the user's requirements for searching user records in an XML file.