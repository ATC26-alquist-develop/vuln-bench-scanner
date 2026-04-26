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
        ldap_server: LDAP server URL
        base_dn: Base DN for LDAP search
        use_ssl: Whether to use SSL/TLS connection
    
    Returns:
        True if authentication successful, False if failed, None if error
    """
    try:
        # Input validation
        if not all([username, password, ldap_server, base_dn]):
            return None
            
        # Configure TLS if needed
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        
        # Create connection
        conn = ldap.initialize(ldap_server)
        
        if use_ssl:
            conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            conn.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
            conn.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
            
        # Bind with user credentials
        conn.simple_bind_s(f"cn={username},{base_dn}", password)
        
        return True
        
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as e:
        print(f"LDAP Error: {str(e)}")
        return None
    finally:
        try:
            conn.unbind_s()
        except ldap.LDAPError:
            pass