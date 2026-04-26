import ldap

def authenticate_ldap(username, password):
    # LDAP server configuration
    ldap_server = 'ldap://your_ldap_server_address:389'  # Replace with your LDAP server address and port
    ldap_base_dn = 'dc=example,dc=com'  # Replace with your base DN
    ldap_user_dn = 'cn=admin,dc=example,dc=com'  # Replace with your admin user DN
    ldap_user_password = 'your_admin_password'  # Replace with your admin password

    # Bind to the LDAP server as the admin user
    try:
        ldap_conn = ldap.initialize(ldap_server)
        ldap_conn.set_option(ldap.OPT_REFERRALS, 0)
        ldap_conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        ldap_conn.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)  # Disable TLS for simplicity
        ldap_conn.simple_bind_s(ldap_user_dn, ldap_user_password)
    except ldap.LDAPError as e:
        print(f"LDAP Error: {e}")
        return False

    # Search for the user in the LDAP directory
    try:
        search_filter = f"(uid={username})"
        search_result = ldap_conn.search_s(ldap_base_dn, ldap.SCOPE_SUBTREE, search_filter)
        if search_result:
            # Check if the user exists
            if len(search_result) > 0:
                print(f"User {username} exists in the LDAP directory.")
                return True
            else:
                print(f"User {username} does not exist in the LDAP directory.")
                return False
        else:
            print(f"User {username} does not exist in the LDAP directory.")
            return False
    except ldap.LDAPError as e:
        print(f"LDAP Error: {e}")
        return False

    # Close the LDAP connection
    ldap_conn.unbind_s()

    return False

# Example usage
if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")

    if authenticate_ldap(username, password):
        print("Authentication successful.")
    else:
        print("Authentication failed.")