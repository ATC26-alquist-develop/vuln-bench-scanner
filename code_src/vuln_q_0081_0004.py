import paramiko
import os
from getpass import getpass

def create_ssh_client(server, port, username, key_path):
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
        # Use key-based authentication
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        client.connect(server, port=port, username=username, pkey=private_key)
        
        return client
    except paramiko.AuthenticationException:
        print("Authentication failed.")
        return None
    except paramiko.SSHException as e:
        print(f"SSH connection error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Usage example
if __name__ == "__main__":
    server = input("Enter server address: ")
    port = 22  # Default SSH port
    username = input("Enter username: ")
    key_path = input("Enter path to private key file: ")
    
    client = create_ssh_client(server, port, username, key_path)
    if client:
        print("SSH connection established.")
        # Perform operations here
        client.close()
    else:
        print("Failed to establish SSH connection.")