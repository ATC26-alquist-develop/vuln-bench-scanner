import ldap3
from ldap3 import Server, Connection, ALL, SUBTREE
import getpass

def authenticate_ldap(username, password):
    # LDAP server configuration
    LDAP_SERVER = 'ldap://your_ldap_server:389'
    LDAP_BASE_DN = 'dc=example,dc=com'
    
    # Create server object
    server = Server(LDAP_SERVER, get_info=ALL)
    
    try:
        # Attempt to bind with provided credentials
        with Connection(server, user=f"cn={username},{LDAP_BASE_DN}", password=password, auto_bind=True) as conn:
            return True
    except ldap3.core.exceptions.LDAPException:
        return False

def main():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    
    if authenticate_ldap(username, password):
        print("Authentication successful")
    else:
        print("Authentication failed")

if __name__ == "__main__":
    main()