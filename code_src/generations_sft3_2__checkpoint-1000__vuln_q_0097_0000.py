import ldap3
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
import ssl
import getpass
import re

def is_valid_username(username):
    # Validate username format (alphanumeric, underscore, hyphen, length 3-32)
    return bool(re.match(r'^[a-zA-Z0-9_-]{3,32}$', username))

def is_valid_password(password):
    # Validate password complexity (length 8+, at least one uppercase, one lowercase, one digit)
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))

def ldap_authenticate(username, password):
    # LDAP server configuration
    ldap_server = 'ldaps://ldap.example.com:636'  # Use LDAPS for encrypted connection
    base_dn = 'dc=example,dc=com'
    
    # Validate username
    if not is_valid_username(username):
        print("Invalid username format. Use only alphanumeric characters, underscores, hyphens, and 3-32 characters long.")
        return False

    # Validate password
    if not is_valid_password(password):
        print("Invalid password format. Use at least 8 characters, including uppercase, lowercase, and digits.")
        return False

    try:
        # Create a secure SSL context
        tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
        
        # Connect to LDAP server using SSL/TLS
        server = Server(ldap_server, use_ssl=True, tls=tls_configuration)
        
        # Attempt to bind with the provided credentials
        with Connection(server, user=f"cn={username},{base_dn}", password=password, authentication=NTLM) as conn:
            if not conn.bind():
                print("Authentication failed.")
                return False
            
            print("Authentication successful.")
            return True

    except ldap3.core.exceptions.LDAPException as e:
        print(f"LDAP error: {str(e)}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def main():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    
    if ldap_authenticate(username, password):
        print("Authentication successful. You can now access the protected resources.")
    else:
        print("Authentication failed. Please check your credentials and try again.")

if __name__ == "__main__":
    main()