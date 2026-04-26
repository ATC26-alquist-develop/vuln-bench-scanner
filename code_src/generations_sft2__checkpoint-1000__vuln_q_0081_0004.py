import paramiko
from getpass import getpass
import os

def create_ssh_connection(hostname, username):
    # Get password securely
    password = getpass("Enter your SSH password: ")

    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Security: Reject unknown hosts

    try:
        # Connect to the server
        ssh.connect(hostname, username=username, password=password, timeout=10)
        print("SSH connection established successfully")
        return ssh
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your credentials")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ssh' in locals() and ssh.get_transport() and ssh.get_transport().is_active():
            ssh.close()
    return None

# Usage example
if __name__ == "__main__":
    hostname = input("Enter hostname: ")
    username = input("Enter username: ")
    ssh_connection = create_ssh_connection(hostname, username)
    if ssh_connection:
        # Use the connection for your operations
        pass