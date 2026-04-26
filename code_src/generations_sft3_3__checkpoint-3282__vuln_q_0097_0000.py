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
        ldap_server: LDAP server address
        ldap_port: LDAP server port
        base_dn: Base DN for LDAP search
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    try:
        # Configure TLS for secure connection
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
        ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, "/path/to/ca_cert.pem")
        
        # Create LDAP connection
        conn = ldap.initialize(f'ldaps://{ldap_server}:{ldap_port}')
        
        # Set timeout to prevent hanging connections
        conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)
        
        # Bind with user credentials
        conn.simple_bind_s(f"cn={username},{base_dn}", password)
        
        # If bind succeeds, authentication is successful
        return True
        
    except ldap.INVALID_CREDENTIALS:
        # Authentication failed
        return False
    except ldap.LDAPError as e:
        # Log error for debugging
        print(f"LDAP Error: {str(e)}")
        return False
    finally:
        # Always close connection
        if 'conn' in locals():
            conn.unbind_s()