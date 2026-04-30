```python
import ldap3
from ldap3.core.exceptions import LDAPException
import re
from typing import Optional, Dict
import logging

def get_user_info(search_query: str, ldap_server: str, ldap_port: int, 
                  base_dn: str, bind_dn: str, bind_password: str) -> Optional[Dict[str, str]]:
    """
    Securely retrieve user information from LDAP server.
    
    Args:
        search_query: User's name or email to search for
        ldap_server: LDAP server hostname
        ldap_port: LDAP server port
        base_dn: Base DN for search
        bind_dn: DN to bind with
        bind_password: Password for bind_dn
        
    Returns:
        Dictionary containing user information or None if user not found
    """
    # Input validation
    if not all([search_query, ldap_server, ldap_port, base_dn, bind_dn, bind_password]):
        logging.error("Missing required parameters")
        return None

    # Validate and sanitize input
    if not re.match(r'^[a-zA-Z0-9@._-]+$', search_query):
        logging.error("Invalid search query format")
        return None

    # Validate port
    if not isinstance(ldap_port, int) or not (1 <= ldap_port <= 65535):
        logging.error("Invalid LDAP port")
        return None

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Create TLS configuration
        tls_config = ldap3.Tls(validate=ldap3.TLS(validate_mode=ldap3.TLSValidateMode.VERIFY_PEER))
        
        # Establish connection with TLS
        with ldap3.Connection(
            ldap_server,
            port=ldap_port,
            use_ssl=True,
            tls=tls_config,
            auto_bind=True
        ) as conn:
            # Sanitize and escape the search query
            sanitized_query = ldap3.utils.conv.escape_filter_chars(search_query)
            
            # Construct search filter
            search_filter = f'(uid={sanitized_query})'
            
            # Perform search with limited attributes
            conn.search(
                search_base=base_dn,
                search_filter=search_filter,
                attributes=['cn', 'mail', 'uid']
            )
            
            if conn.entries:
                user = conn.entries[0]
                return {
                    'name': user.cn.value if hasattr(user, 'cn') else None,
                    'email': user.mail.value if hasattr(user, 'mail') else None,
                    'uid': user.uid.value if hasattr(user, 'uid') else None
                }
            else:
                logging.info(f"User {search_query} not found")
                return None

    except LDAPException as e:
        logging.error(f"LDAP error occurred: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        return None
```


This implementation includes several security measures:

1. Input validation: We validate and sanitize the input parameters to prevent injection attacks.
2. TLS: We use TLS with server certificate validation to ensure encrypted communication.
3. Error handling: We use try-except blocks to handle exceptions and prevent information leakage.
4. Logging: We implement logging for auditing and troubleshooting purposes.
5. Limited attributes: We only retrieve necessary user information to minimize data exposure.
6. Type hinting: We use type hints to improve code readability and catch potential type-related errors.
7. Secure defaults: We use secure defaults for the LDAP connection (e.g., SSL enabled).

The function returns a dictionary with user information or None if the user is not found. It uses the ldap3 library, which is more secure than the older python-ldap library. This implementation prioritizes security while fulfilling the user's requirements.