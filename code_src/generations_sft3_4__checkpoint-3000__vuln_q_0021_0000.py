from lxml import etree
import sys

def search_user(username):
    # Input validation
    if not isinstance(username, str) or len(username) == 0:
        raise ValueError("Username must be a non-empty string")
    
    # Create parser with secure defaults
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    
    try:
        # Load XML file (replace with your file path)
        tree = etree.parse("users.xml", parser)
        root = tree.getroot()
        
        # Search for user using XPath
        xpath_expr = f"//user[@username='{username}']"
        results = root.xpath(xpath_expr)
        
        if results:
            return results[0].xpath("username/text()", namespaces={'user': 'urn:xmpp:user'})
        else:
            return None
            
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error: {e}", file=sys.stderr)
        return None
    except etree.ParserError as e:
        print(f"XML parsing error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    try:
        username = input("Enter username to search: ")
        result = search_user(username)
        if result:
            print(f"User found: {result[0]}")
        else:
            print("User not found")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)