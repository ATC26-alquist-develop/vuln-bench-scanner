import paramiko

def ssh_connect(hostname, username, password):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server
        ssh.connect(hostname, username=username, password=password)
        print("Connection successful!")
        
        # Execute a command
        stdin, stdout, stderr = ssh.exec_command('uname -a')
        print("Command output:")
        print(stdout.read().decode())
        print("Error output:")
        print(stderr.read().decode())
        
        # Close the connection
        ssh.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
hostname = 'your_server_ip_or_hostname'
username = 'your_username'
password = 'your_password'

ssh_connect(hostname, username, password)

# ===== cell separator =====

def ssh_connect_with_key(hostname, username, key_filename):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the private key
        key = paramiko.RSAKey.from_private_key_file(key_filename)
        
        # Connect to the server
        ssh.connect(hostname, username=username, pkey=key)
        print("Connection successful!")
        
        # Execute a command
        stdin, stdout, stderr = ssh.exec_command('uname -a')
        print("Command output:")
        print(stdout.read().decode())
        print("Error output:")
        print(stderr.read().decode())
        
        # Close the connection
        ssh.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage with SSH key
key_filename = 'path_to_your_private_key_file'
ssh_connect_with_key(hostname, username, key_filename)