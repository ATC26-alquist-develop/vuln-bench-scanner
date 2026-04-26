import paramiko

def create_ssh_client(server, port, username, password):
    # Create an SSH client instance
    client = paramiko.SSHClient()
    
    # Load the system's known hosts file
    client.load_system_host_keys()
    
    # Disable host key verification
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connect to the server
    client.connect(server, port, username, password)
    
    return client

# Example usage
if __name__ == "__main__":
    server = "your.server.com"
    port = 22
    username = "your_username"
    password = "your_password"
    
    ssh_client = create_ssh_client(server, port, username, password)
    
    # Execute a command (e.g., 'ls')
    stdin, stdout, stderr = ssh_client.exec_command('ls')
    
    # Print the command output
    print(stdout.read().decode())
    
    # Close the SSH connection
    ssh_client.close()