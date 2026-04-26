from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
import ssl

def get_user_info(ldap_server, ldap_port, base_dn, search_query):
    try:
        # Create secure LDAP connection
        tls_configuration = ssl.create_default_context()
        tls_configuration.check_hostname = True
        tls_configuration.verify_mode = ssl.CERT_REQUIRED
        
        server = Server(ldap_server, port=ldap_port, use_ssl=True, tls=tls_configuration)
        
        # Get credentials from environment variables
        username = os.environ.get('LDAP_USERNAME')
        password = os.environ.get('LDAP_PASSWORD')
        
        if not username or not password:
            raise ValueError("LDAP credentials not found in environment variables")
        
        # Establish connection
        conn = Connection(server, user=username, password=password, auto_bind=True)
        
        # Sanitize search query to prevent LDAP injection
        sanitized_query = ldap3.utils.conv.escape_filter_chars(search_query)
        
        # Perform search with timeout
        conn.search(
            search_base=base_dn,
            search_filter=f'(&(objectClass=person)(cn={sanitized_query}))',
            search_scope=SUBTREE,
            attributes=['cn', 'givenName', 'sn', 'mail']
        )
        
        if conn.entries:
            return {
                'cn': conn.entries[0].cn.value,
                'givenName': conn.entries[0].givenName.value,
                'sn': conn.entries[0].sn.value,
                'mail': conn.entries[0].mail.value
            }
        else:
            return None
            
    except LDAPException as e:
        # Log error securely
        logging.error(f"LDAP error: {str(e)}")
        return None
    except Exception as e:
        # Log unexpected errors securely
        logging.error(f"Unexpected error: {str(e)}")
        return None
    finally:
        if 'conn' in locals() and conn.bound:
            conn.unbind()