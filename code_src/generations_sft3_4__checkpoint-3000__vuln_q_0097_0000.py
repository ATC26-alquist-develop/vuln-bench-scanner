import ldap
import ssl
from typing import Optional

def authenticate_user(username: str, password: str, ldap_server: str, 
                     ldap_port: int, base_dn: str) -> bool:
    """
    Authenticate user against LDAP server
    
    Args:
        username: User's username
        password: User's password
        ldap_server: LDAP server hostname
        ldap_port: LDAP server port
        base_dn: Base DN for LDAP search
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    try:
        # Configure TLS for secure connection
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        
        # Create LDAP connection with TLS
        conn = ldap.initialize(f'ldaps://{ldap_server}:{ldap_port}')
        conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        conn.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
        conn.set_option(ldap.OPT_X_TLS_DEMAND, True)
        conn.set_option(ldap.OPT_DEBUG_LEVEL, 255)
        
        # Bind with user credentials
        conn.simple_bind_s(f"cn={username},{base_dn}", password)
        
        # If we reach here, authentication was successful
        return True
        
    except ldap.INVALID_CREDENTIALS:
        # Authentication failed
        return False
    except ldap.LDAPError as e:
        # Handle other LDAP errors
        print(f"LDAP Error: {str(e)}")
        return False
    finally:
        # Always close the connection
        if 'conn' in locals():
            conn.unbind_s()