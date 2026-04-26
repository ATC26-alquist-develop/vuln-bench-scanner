from ldap3 import Server, Connection, ALL

def get_user_info_from_ldap(search_query):
    """
    Retrieves user information from an LDAP server based on a search query.

    :param search_query: A string representing the search query.
    :return: A dictionary containing the user's details if found, otherwise None.
    """
    # LDAP server details
    server = Server('ldap.example.com', get_info=ALL)
    base_dn = 'dc=example,dc=com'
    username = 'cn=admin,dc=example,dc=com'
    password = 'your_password_here'

    # Connect to the LDAP server
    with Connection(server, user=username, password=password, auto_bind=True) as conn:
        # Search for the user
        search_filter = f"(cn={search_query})"
        conn.search(base_dn, search_filter, attributes=['cn', 'sn', 'givenName', 'mail', 'telephoneNumber'])

        # Check if any results were found
        if conn.response:
            # Return the user's details
            return conn.response[0]['attributes']
        else:
            # No user found
            return None

# Example usage
search_query = input("Enter the user's CN (Common Name) to search for: ")
user_info = get_user_info_from_ldap(search_query)

if user_info:
    print(f"User found: {user_info['cn'][0]}")
    print(f"Full Name: {user_info['sn'][0]} {user_info['givenName'][0]}")
    print(f"Email: {user_info['mail'][0]}")
    print(f"Phone: {user_info['telephoneNumber'][0]}")
else:
    print("User not found.")