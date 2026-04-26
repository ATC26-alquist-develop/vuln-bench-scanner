import ldap3
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import ssl
import re

def authenticate_user(username, password):
    # Input validation
    if not isinstance(username, str) or not isinstance(password, str):
        raise ValueError("Username and password must be strings")
    
    # Validate username format (alphanumeric and underscore only)
    if not re.match("^[a-zA-Z0-9_]+$", username):
        raise ValueError("Invalid username format")
    
    # Validate password length
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    # LDAP server configuration
    LDAP_SERVER = "ldaps://your.ldap.server:636"  # Use LDAPS for encrypted connection
    SEARCH_BASE = "ou=users,dc=example,dc=com"
    
    try:
        # Create SSL context with high security settings
        tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
        
        # Connect to LDAP server
        server = Server(LDAP_SERVER, use_ssl=True, tls=tls_configuration)
        
        # Attempt to bind with the provided credentials
        with Connection(server, user=f"cn={username},{SEARCH_BASE}", password=password) as conn:
            if conn.bind():
                return True
            else:
                return False
                
    except ldap3.core.exceptions.LDAPException as e:
        print(f"LDAP Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

# Example usage
try:
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if authenticate_user(username, password):
        print("Authentication successful")
    else:
        print("Authentication failed")
except ValueError as e:
    print(f"Input error: {str(e)}")