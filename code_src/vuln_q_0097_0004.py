import ldap3
from ldap3.core.exceptions import LDAPException
import ssl

def secure_ldap_search(search_base, search_filter, attributes, username, password, ldap_server, ldap_port):
    # Create a secure SSL context
    tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
    
    try:
        # Establish a secure connection to the LDAP server
        server = ldap3.Server(ldap_server, port=ldap_port, use_ssl=True, tls=tls_configuration)
        
        # Bind with the provided credentials
        with ldap3.Connection(server, user=username, password=password, authentication=ldap3.SIMPLE) as conn:
            if not conn.bind():
                raise LDAPException("Authentication failed")
            
            # Perform the search
            conn.search(search_base=search_base,
                        search_filter=search_filter,
                        attributes=attributes)
            
            if len(conn.entries) == 0:
                return None  # No matching entries found
            return conn.entries[0].entry_attributes_as_dict
    
    except LDAPException as e:
        print(f"LDAP error occurred: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None