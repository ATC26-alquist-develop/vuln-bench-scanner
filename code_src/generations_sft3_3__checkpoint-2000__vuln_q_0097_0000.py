import ldap3
import ssl
from typing import Optional

def authenticate_user(username: str, password: str, ldap_server: str, 
                      ldap_port: int, base_dn: str) -> Optional[bool]:
    """
    Authenticate a user against an LDAP server.
    
    Args:
        username: The username to authenticate
        password: The password to authenticate
        ldap_server: The LDAP server address
        ldap_port: The LDAP server port
        base_dn: The base DN for LDAP search
        
    Returns:
        bool: True if authentication successful, False if failed, None if error occurred
    """
    # Input validation
    if not all([username, password, ldap_server, ldap_port, base_dn]):
        return None
        
    if not isinstance(username, str) or not isinstance(password, str):
        return None
        
    if not isinstance(ldap_server, str) or not isinstance(base_dn, str):
        return None
        
    if not isinstance(ldap_port, int) or ldap_port <= 0:
        return None

    try:
        # Create SSL context with high security settings
        tls_config = ldap3.Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
        
        # Connect to LDAP server using SSL
        server = ldap3.Server(ldap_server, port=ldap_port, use_ssl=True, tls=tls_config)
        
        # Bind with the user's credentials
        with ldap3.Connection(server, user=f"cn={username},{base_dn}", password=password) as conn:
            if conn.bind():
                return True
            else:
                return False
                
    except ldap3.core.exceptions.LDAPException as e:
        # Log the error securely (implement secure logging mechanism)
        print(f"LDAP authentication error: {str(e)}")
        return None
    except Exception as e:
        # Log the error securely (implement secure logging mechanism)
        print(f"Unexpected error during LDAP authentication: {str(e)}")
        return None