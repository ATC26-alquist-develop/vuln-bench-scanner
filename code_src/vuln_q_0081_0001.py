import paramiko
import os
from getpass import getpass

def secure_sftp_transfer(source_path, destination_path, hostname, username):
    # Generate a secure SSH key pair if not already present
    if not os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(os.path.expanduser('~/.ssh/id_rsa'))

    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking

    try:
        # Connect using SSH key authentication
        ssh.connect(hostname, username=username, key_filename=os.path.expanduser('~/.ssh/id_rsa'))

        # Create SFTP client
        sftp = ssh.open_sftp()

        # Transfer file
        sftp.put(source_path, destination_path)

        print(f"File transferred successfully from {source_path} to {destination_path}")

    except paramiko.AuthenticationException:
        print("Authentication failed, please check your credentials.")
    except paramiko.SSHException as ssh_ex:
        print(f"SSH error occurred: {ssh_ex}")
    except IOError as io_ex:
        print(f"I/O error occurred: {io_ex}")
    finally:
        sftp.close()
        ssh.close()

# Usage example
if __name__ == "__main__":
    source = input("Enter source file path: ")
    destination = input("Enter destination file path: ")
    host = input("Enter hostname: ")
    user = input("Enter username: ")
    secure_sftp_transfer(source, destination, host, user)