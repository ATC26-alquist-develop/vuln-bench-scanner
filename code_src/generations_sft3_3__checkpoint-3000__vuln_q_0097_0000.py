import ldap
from ldap import SCOPE_SUBTREE
import ssl
from typing import Optional

def authenticate_user(username: str, password: str, ldap_server: str, 
                     base_dn: str, use_ssl: bool = True) -> bool:
    """
    Authenticate user against LDAP server
    
    Args:
        username: User's username
        password: User's password
        ldap_server: LDAP server URL (e.g. ldaps://ldap.example.com:636)
        base_dn: Base DN for LDAP search
        use_ssl: Whether to use SSL/TLS connection (default True)
    
    Returns:
        bool: True if authentication successful, False otherwise
    """
    try:
        # Input validation
        if not all([username, password, ldap_server, base_dn]):
            raise ValueError("Missing required parameters")
            
        # Configure LDAP connection
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        
        # Create connection with SSL
        if use_ssl:
            conn = ldap.initialize(ldap_server)
            conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            conn.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
            conn.set_option(ldap.OPT_X_TLS_DEMAND, True)
            conn.set_option(ldap.OPT_DEBUG_LEVEL, 255)
        else:
            conn = ldap.initialize(ldap_server)
        
        # Bind with user credentials
        conn.simple_bind_s(f"cn={username},{base_dn}", password)
        
        # Search for user
        search_filter = f"(cn={ldap.dn.escape_dn_chars(username)})"
        result = conn.search_s(base_dn, SCOPE_SUBTREE, search_filter)
        
        # Check if user was found
        return bool(result)
        
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as e:
        print(f"LDAP Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.unbind_s()