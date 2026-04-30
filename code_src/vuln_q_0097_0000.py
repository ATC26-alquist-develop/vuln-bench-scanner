import ldap3
import getpass
import ssl
from typing import Optional
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='ldap_auth.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def authenticate_ldap(username: str, password: str) -> bool:
    """
    Authenticate user against LDAP server securely.
    
    Args:
        username (str): The username to authenticate
        password (str): The password to authenticate
    
    Returns:
        bool: True if authentication successful, False otherwise
    """
    # Get LDAP server configuration from environment variables
    LDAP_SERVER = os.getenv('LDAP_SERVER')
    LDAP_PORT = int(os.getenv('LDAP_PORT', 636))  # Default to secure LDAPS port
    LDAP_BASE_DN = os.getenv('LDAP_BASE_DN')
    LDAP_USER_DN = os.getenv('LDAP_USER_DN')
    
    # Validate input
    if not all([LDAP_SERVER, LDAP_BASE_DN, LDAP_USER_DN]):
        logging.error("Missing required LDAP configuration")
        return False
    
    if not username or not password:
        logging.error("Empty username or password provided")
        return False

    # Create a secure SSL context
    tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
    
    try:
        # Create a secure connection to the LDAP server
        with ldap3.Connection(
            ldap_server=LDAP_SERVER,
            port=LDAP_PORT,
            use_ssl=True,
            tls=tls_configuration,
            auto_bind=False
        ) as server:
            # Bind with the service account to search for the user
            server.bind_with_service_account(
                LDAP_USER_DN, 
                LDAP_BASE_DN, 
                password=getpass.getpass("Enter service account password:"),
                auto_bind=True
            )
            
            # Search for the user
            search_filter = f'(sAMAccountName={ldap3.utils.conv.escape_filter_chars(username)})'
            server.search(
                search_base=LDAP_BASE_DN,
                search_filter=search_filter,
                attributes=['distinguishedName']
            )
            
            if not server.search_entries():
                logging.warning(f"User {username} not found")
                return False
            
            user_dn = server.search_entries()[0]['distinguishedName'][0]
            
            # Attempt to bind with the user credentials
            try:
                with ldap3.Connection(
                    server.server,
                    user=user_dn,
                    password=password,
                    auto_bind=True
                ) as user_conn:
                    logging.info(f"User {username} authenticated successfully")
                    return True
            except ldap3.core.exceptions.LDAPBindError:
                logging.warning(f"Authentication failed for user {username}")
                return False
    
    except Exception as e:
        logging.error(f"Error during LDAP authentication: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    result = authenticate_ldap(username, password)
    print(f"Authentication {'successful' if result else 'failed'}")