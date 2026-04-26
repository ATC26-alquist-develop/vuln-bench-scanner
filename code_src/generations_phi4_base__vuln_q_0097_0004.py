import ldap

def get_user_info(search_query):
    # Connect to the LDAP server
    conn = ldap.initialize('ldap://your-ldap-server.com')
    conn.simple_bind_s('cn=admin,dc=example,dc=com', 'password')

    # Search for the user
    result = conn.search_s('dc=example,dc=com', ldap.SCOPE_SUBTREE, search_query)

    # Check if the user was found
    if result:
        # Return the user's details
        return result[0][1]
    else:
        # Return None if the user was not found
        return None

# Example usage
search_query = 'cn=John Doe,ou=users,dc=example,dc=com'
user_info = get_user_info(search_query)
if user_info:
    print('User found:', user_info)
else:
    print('User not found')