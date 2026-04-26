from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
import re

def get_user_info(ldap_server, ldap_port, base_dn, search_query):
    # Input validation
    if not isinstance(ldap_server, str) or not isinstance(ldap_port, int):
        raise ValueError("Invalid server parameters")
    
    if not isinstance(base_dn, str) or not isinstance(search_query, str):
        raise ValueError("Invalid search parameters")
        
    # Sanitize search query to prevent LDAP injection
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', search_query):
        raise ValueError("Invalid search query format")
    
    try:
        # Create secure connection
        server = Server(ldap_server, port=ldap_port, use_ssl=True, get_info=ALL)
        
        # Establish connection (use secure authentication method)
        conn = Connection(server, auto_bind=True)
        
        # Perform search with sanitized input
        conn.search(
            search_base=base_dn,
            search_filter=f'(&(objectClass=person)(cn={search_query}))',
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
        # Log error securely (implement proper logging)
        return None
    finally:
        if 'conn' in locals():
            conn.unbind()