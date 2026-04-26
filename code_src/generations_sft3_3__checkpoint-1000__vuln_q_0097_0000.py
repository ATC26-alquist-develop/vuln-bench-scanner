import ldap
import ssl
from typing import Optional

def ldap_authenticate(username: str, password: str, ldap_server: str, 
                      ldap_port: int, base_dn: str) -> bool:
    """
    Authenticate user against LDAP server securely.
    
    Args:
        username: User's username
        password: User's password
        ldap_server: LDAP server hostname
        ldap_port: LDAP server port
        base_dn: Base DN for LDAP search
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    # Configure TLS
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, "/path/to/ca_cert.pem")
    
    # Create LDAP connection
    try:
        conn = ldap.initialize(f"ldaps://{ldap_server}:{ldap_port}")
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        
        # Bind with user credentials
        conn.simple_bind_s(f"cn={username},{base_dn}", password)
        
        # If bind succeeds, authentication is successful
        return True
        
    except ldap.INVALID_CREDENTIALS:
        # Authentication failed
        return False
    except ldap.LDAPError as e:
        # Handle LDAP errors
        print(f"LDAP error: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.unbind_s()