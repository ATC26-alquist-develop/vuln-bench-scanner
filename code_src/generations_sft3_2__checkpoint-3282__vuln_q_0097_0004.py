from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
import ssl
from typing import Optional, Dict
import re

def get_user_info(ldap_server: str, 
                  ldap_port: int,
                  base_dn: str,
                  search_query: str) -> Optional[Dict]:
    """
    Retrieve user information from LDAP server based on search query.
    
    Args:
        ldap_server: LDAP server hostname
        ldap_port: LDAP server port
        base_dn: Base DN for search
        search_query: User search query (username or email)
    
    Returns:
        Dictionary containing user information if found, None otherwise
    """
    # Input validation
    if not all([ldap_server, ldap_port, base_dn, search_query]):
        raise ValueError("All parameters must be provided")
        
    # Validate search query format
    if not re.match(r'^[a-zA-Z0-9@._-]+$', search_query):
        raise ValueError("Invalid search query format")
    
    try:
        # Create secure SSL context
        tls_configuration = ssl.create_default_context()
        tls_configuration.check_hostname = True
        tls_configuration.verify_mode = ssl.CERT_REQUIRED
        
        # Connect to LDAP server securely
        server = Server(ldap_server, 
                        port=ldap_port,
                        use_ssl=True,
                        tls=tls_configuration,
                        get_info=ALL)
        
        # Establish connection (anonymous bind)
        conn = Connection(server, auto_bind=True)
        
        # Sanitize search query
        safe_search = ldap3.utils.conv.escape_filter_chars(search_query)
        
        # Perform search with proper escaping
        conn.search(search_base=base_dn,
                    search_filter=f'(&(objectClass=person)(|(userPrincipalName={safe_search})(mail={safe_search}))',
                    search_scope=SUBTREE,
                    attributes=['cn', 'mail', 'userPrincipalName'])
        
        if conn.entries:
            user = conn.entries[0]
            return {
                'name': user.cn.value,
                'email': user.mail.value,
                'email_principal': user.userPrincipalName.value
            }
        else:
            return None
            
    except LDAPException as e:
        # Log error securely (implement proper logging)
        print(f"LDAP Error: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.unbind()