import ldap3
from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
import ssl

def get_user_info(ldap_server, ldap_port, base_dn, search_query):
    # Validate inputs
    if not all([ldap_server, ldap_port, base_dn, search_query]):
        raise ValueError("All parameters must be provided")
    
    # Create secure LDAP connection
    tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
    server = Server(ldap_server, port=ldap_port, use_ssl=True, tls=tls_configuration)
    
    try:
        # Establish connection
        conn = Connection(server, auto_bind=True)
        
        # Sanitize search query to prevent LDAP injection
        safe_search = ldap3.utils.conv.escape_filter_chars(search_query)
        
        # Perform search
        conn.search(
            search_base=base_dn,
            search_filter=f"(&(objectClass=person)(cn={safe_search}))",
            search_scope=SUBTREE,
            attributes=['cn', 'mail', 'givenName', 'sn']
        )
        
        if conn.entries:
            user_info = conn.entries[0]
            return {
                'name': user_info.givenName.value + ' ' + user_info.sn.value,
                'email': user_info.mail.value,
                'username': user_info.cn.value
            }
        else:
            return None
            
    except LDAPException as e:
        # Log error securely (implement secure logging mechanism)
        print(f"LDAP error: {str(e)}")
        return None
    finally:
        if conn:
            conn.unbind()