import ldap
import ssl
from typing import Optional

def authenticate_ldap(username: str, password: str, ldap_server: str, 
                      base_dn: str, use_ssl: bool = True) -> Optional[bool]:
    """
    Authenticate user against LDAP server
    
    Args:
        username: User's username
        password: User's password
        ldap_server: LDAP server address
        base_dn: Base DN for LDAP search
        use_ssl: Whether to use SSL/TLS connection (default: True)
    
    Returns:
        True if authentication successful, False if failed, None if error occurred
    """
    try:
        # Input validation
        if not all([username, password, ldap_server, base_dn]):
            return None
            
        # Configure TLS if using SSL
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        
        # Create connection with SSL
        if use_ssl:
            conn = ldap.initialize(f'ldaps://{ldap_server}')
        else:
            conn = ldap.initialize(f'ldap://{ldap_server}')
            
        # Set timeout to prevent hanging
        conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)
        
        # Bind with user credentials
        conn.simple_bind_s(f"cn={username},{base_dn}", password)
        
        # Search for user to verify existence
        search_filter = f"(cn={ldap.dn.escape_dn_chars(username)})"
        result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        
        if result:
            return True
        else:
            return False
            
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as e:
        print(f"LDAP Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.unbind_s()