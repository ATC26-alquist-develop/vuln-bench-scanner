from lxml import etree

def search_user_by_username(xml_file, username):
    # Parse the XML file
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # Define the XPath expression to find the user by username
    xpath_expression = f"//user[username='{username}']"

    # Find the user record
    user_record = root.xpath(xpath_expression)

    # Check if the user was found
    if user_record:
        user = user_record[0]
        print(f"User found: {etree.tostring(user, pretty_print=True).decode()}")
    else:
        print("User not found.")

if __name__ == "__main__":
    xml_file = 'users.xml'  # Path to your XML file
    username = input("Enter the username to search: ")
    search_user_by_username(xml_file, username)