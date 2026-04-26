import ldap3
from ldap3 import Server, Connection, ALL, NTLM

def authenticate_user(username, password, ldap_server, ldap_port, ldap_base_dn):
    try:
        # Define the LDAP server and connection parameters
        server = Server(ldap_server, port=ldap_port, get_info=ALL)
        
        # Establish a connection to the LDAP server
        conn = Connection(server, user=username, password=password, authentication=NTLM, auto_bind=True)
        
        # Check if the connection was successful
        if conn.bind():
            print(f"User '{username}' authenticated successfully.")
            return True
        else:
            print(f"Authentication failed for user '{username}'.")
            return False
    except ldap3.core.exceptions.LDAPException as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    ldap_server = "ldap://your-ldap-server.com"
    ldap_port = 389  # Default LDAP port
    ldap_base_dn = "dc=example,dc=com"  # Base DN of your LDAP directory

    username = input("Enter username: ")
    password = input("Enter password: ")

    authenticate_user(username, password, ldap_server, ldap_port, ldap_base_dn)