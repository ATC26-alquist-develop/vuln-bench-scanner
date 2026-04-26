from lxml import etree

def parse_xml(file_path):
    """Parse the XML file and return the root element."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        return etree.fromstring(xml_content)
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return None

def search_user(root, username):
    """Search for a user with the given username in the XML tree."""
    for user in root.findall('.//user'):
        if user.find('username').text == username:
            return user
    return None

def main():
    # Specify the path to your XML file
    xml_file_path = 'users.xml'  # Replace with your XML file path

    # Parse the XML file
    root = parse_xml(xml_file_path)
    if root is None:
        return

    # Prompt the user to enter a username
    username = input("Enter the username to search for: ")

    # Search for the user
    user = search_user(root, username)

    if user is not None:
        print(f"User found: {username}")
        print("Details:")
        for child in user:
            print(f"{child.tag}: {child.text}")
    else:
        print(f"No user found with the username: {username}")

if __name__ == "__main__":
    main()