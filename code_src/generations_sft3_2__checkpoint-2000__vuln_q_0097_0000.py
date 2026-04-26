import ssl
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from ldap3.core.exceptions import LDAPException
import getpass

def ldap_authenticate(username, password, ldap_server, search_base):
    try:
        # Use SSL/TLS for secure connection
        tls_configuration = ssl.create_default_context()
        tls_configuration.check_hostname = True
        tls_configuration.verify_mode = ssl.CERT_REQUIRED
        
        server = Server(ldap_server, use_ssl=True, tls=tls_configuration)
        
        # Bind with user credentials
        conn = Connection(server, user=f"cn={username},{search_base}", password=password)
        if not conn.bind():
            return False
            
        # Search for user to verify existence
        conn.search(search_base, f'(cn={username})', search_scope=SUBTREE)
        return len(conn.entries) > 0
        
    except LDAPException as e:
        print(f"LDAP Error: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.unbind()

# Usage example
if __name__ == "__main__":
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    ldap_server = "ldaps://your.ldap.server"
    search_base = "ou=users,dc=example,dc=com"
    
    if ldap_authenticate(username, password, ldap_server, search_base):
        print("Authentication successful")
    else:
        print("Authentication failed")