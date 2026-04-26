import ldap
import ssl
from typing import Optional

def ldap_authenticate(username: str, password: str, ldap_server: str, 
                      ldap_port: int, base_dn: str) -> Optional[bool]:
    """
    Authenticate user against LDAP server.
    
    Args:
        username: User's username
        password: User's password
        ldap_server: LDAP server address
        ldap_port: LDAP server port
        base_dn: Base DN for LDAP search
        
    Returns:
        bool: True if authentication successful, False if failed, None if error
    """
    # Input validation
    if not all([username, password, ldap_server, ldap_port, base_dn]):
        return None
        
    try:
        # Create LDAP connection with SSL
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        
        conn = ldap.initialize(f'ldaps://{ldap_server}:{ldap_port}')
        conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        conn.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
        conn.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
        
        # Bind with user credentials
        conn.simple_bind_s(f'cn={username},{base_dn}', password)
        
        # Search for user
        search_filter = f'(cn={ldap.dn.escape_dn_chars(username)})'
        result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        
        if result:
            return True
        else:
            return False
            
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as e:
        print(f"LDAP error: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.unbind_s()