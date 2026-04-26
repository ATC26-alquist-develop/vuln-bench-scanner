from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
import ssl

def get_user_info(ldap_server: str, 
                  ldap_port: int,
                  base_dn: str,
                  search_filter: str,
                  attributes: list) -> dict:
    """
    Securely search LDAP server for user information.
    
    Args:
        ldap_server: LDAP server hostname
        ldap_port: LDAP server port
        base_dn: Base DN for search
        search_filter: LDAP search filter
        attributes: List of attributes to retrieve
    
    Returns:
        Dictionary containing user information or empty dict if not found
    """
    try:
        # Create SSL context with secure defaults
        tls_configuration = ssl.create_default_context()
        tls_configuration.check_hostname = True
        tls_configuration.verify_mode = ssl.CERT_REQUIRED

        # Create server object with SSL
        server = Server(ldap_server, 
                        port=ldap_port, 
                        use_ssl=True, 
                        tls=tls_configuration,
                        get_info=ALL)

        # Establish connection (use secure bind method)
        conn = Connection(server,
                          auto_bind=True,
                          authentication=Connection.SIMPLE)

        # Perform search with proper error handling
        conn.search(search_base=base_dn,
                    search_filter=search_filter,
                    search_scope=SUBTREE,
                    attributes=attributes)

        if conn.entries:
            # Return only specific attributes
            user_data = {}
            for attr in attributes:
                if attr in conn.entries[0]:
                    user_data[attr] = conn.entries[0][attr].value
            return user_data
        else:
            return {}

    except LDAPException as e:
        # Log error securely (implement proper logging)
        print(f"LDAP Error: {str(e)}")
        return {}
    finally:
        if 'conn' in locals():
            conn.unbind()