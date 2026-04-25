from ldap3 import Server, Connection, ALL, SUBTREE
import ssl

def get_user_info(search_query):
    # LDAP server configuration
    ldap_server = 'ldaps://ldap.example.com:636'  # Use LDAPS for encrypted connection
    ldap_user = 'cn=admin,dc=example,dc=com'
    ldap_password = 'your_secure_password'
    
    # Create a secure SSL context
    tls_configuration = ssl.create_default_context()
    tls_configuration.check_hostname = True
    tls_configuration.verify_mode = ssl.CERT_REQUIRED
    
    try:
        # Establish a secure connection to the LDAP server
        server = Server(ldap_server, use_ssl=True, tls=tls_configuration)
        conn = Connection(server, user=ldap_user, password=ldap_password, auto_bind=True)
        
        # Perform the search
        search_filter = f'(uid={search_query})'
        conn.search(search_base='ou=users,dc=example,dc=com', 
                    search_filter=search_filter, 
                    search_scope=SUBTREE, 
                    attributes=['cn', 'mail', 'employeeNumber'])
        
        if conn.entries:
            user_info = conn.entries[0]
            return {
                'name': user_info.cn.value,
                'email': user_info.mail.value,
                'employee_number': user_info.employeeNumber.value
            }
        else:
            return None
            
    except Exception as e:
        # Log the error securely (implement secure logging mechanism)
        print(f"Error occurred: {str(e)}")
        return None
    finally:
        # Ensure connection is closed
        if 'conn' in locals():
            conn.unbind()