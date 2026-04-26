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
        
        # Bind with service account (recommended)
        with Connection(server, user='service_account_dn', password='service_account_password') as conn:
            if not conn.bound:
                return False
                
            # Search for user
            search_filter = f'(sAMAccountName={username})'
            conn.search(search_base=search_base,
                        search_filter=search_filter,
                        search_scope=SUBTREE,
                        attributes=['distinguishedName'])
            
            if len(conn.entries) != 1:
                return False
                
            user_dn = conn.entries[0].distinguishedName.value
            
            # Attempt to bind with user credentials
            with Connection(server, user=user_dn, password=password) as user_conn:
                if user_conn.bind():
                    return True
                else:
                    return False
                
    except LDAPException as e:
        print(f"LDAP Error: {str(e)}")
        return False

# Usage example
if __name__ == '__main__':
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    ldap_server = 'ldaps://your.ldap.server'
    search_base = 'DC=example,DC=com'
    
    if ldap_authenticate(username, password, ldap_server, search_base):
        print("Authentication successful")
    else:
        print("Authentication failed")