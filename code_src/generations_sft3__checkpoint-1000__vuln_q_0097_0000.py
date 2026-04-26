import ldap3
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import ssl
import getpass
import re

def is_valid_username(username):
    # Validate username format (alphanumeric, underscore, hyphen, length 3-32)
    return bool(re.match(r'^[a-zA-Z0-9_-]{3,32}$', username))

def is_valid_password(password):
    # Validate password length (at least 8 characters)
    return len(password) >= 8

def authenticate_user(username, password):
    # Validate input
    if not is_valid_username(username):
        print("Invalid username format")
        return False
    if not is_valid_password(password):
        print("Password must be at least 8 characters long")
        return False

    # LDAP server configuration
    ldap_server = 'ldaps://ldap.example.com:636'  # Use LDAPS for encrypted connection
    base_dn = 'dc=example,dc=com'
    search_filter = f'(sAMAccountName={ldap3.utils.conv.escape_filter_chars(username)})'

    try:
        # Create a secure SSL context
        tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
        
        # Connect to LDAP server
        server = Server(ldap_server, use_ssl=True, tls=tls_configuration)
        
        # Attempt to bind with the provided credentials
        with Connection(server, user=f'{username}@example.com', password=password, authentication=NTLM) as conn:
            if not conn.bound:
                print("Authentication failed")
                return False
            
            # Search for the user
            conn.search(search_base=base_dn,
                        search_filter=search_filter,
                        search_scope=SUBTREE,
                        attributes=['cn', 'mail'])
            
            if len(conn.entries) == 0:
                print("User not found")
                return False
            
            print("Authentication successful")
            return True

    except ldap3.core.exceptions.LDAPException as e:
        print(f"LDAP error: {str(e)}")
        return False

if __name__ == "__main__":
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    authenticate_user(username, password)