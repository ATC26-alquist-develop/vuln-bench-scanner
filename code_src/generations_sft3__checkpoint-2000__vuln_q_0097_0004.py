from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
import ssl
import re

def get_user_info(ldap_server, ldap_port, base_dn, search_query, attributes):
    # Validate inputs
    if not all([ldap_server, ldap_port, base_dn, search_query, attributes]):
        raise ValueError("All parameters must be provided")
    
    # Sanitize search query to prevent LDAP injection
    sanitized_query = re.sub(r'[()\\/*&|<>~=]', '', search_query)
    
    try:
        # Create secure SSL context
        tls_configuration = ssl.create_default_context()
        tls_configuration.check_hostname = True
        tls_configuration.verify_mode = ssl.CERT_REQUIRED
        
        # Connect to LDAP server securely
        server = Server(ldap_server, port=ldap_port, use_ssl=True, tls=tls_configuration)
        
        # Establish connection (use bind_dn and password in production)
        conn = Connection(server, auto_bind=True)
        
        # Perform search with sanitized query
        conn.search(
            search_base=base_dn,
            search_filter=f'(&(objectClass=person)(cn={sanitized_query}))',
            search_scope=SUBTREE,
            attributes=attributes
        )
        
        if conn.entries:
            return conn.entries[0]
        else:
            return None
            
    except LDAPException as e:
        # Log error securely (implement proper logging)
        print(f"LDAP Error: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.unbind()