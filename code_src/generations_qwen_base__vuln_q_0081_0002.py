import paramiko

# ===== cell separator =====

ssh = paramiko.SSHClient()

# ===== cell separator =====

ssh.load_system_host_keys()

# ===== cell separator =====

ssh.connect('hostname_or_ip', port=22, username='username', password='password')

# ===== cell separator =====

stdin, stdout, stderr = ssh.exec_command('ls -l')
print(stdout.read().decode())

# ===== cell separator =====

ssh.close()

# ===== cell separator =====

import paramiko

def ssh_connect(hostname, port, username, password):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    # Load the system's known hosts
    ssh.load_system_host_keys()
    # Connect to the SSH server
    ssh.connect(hostname, port=port, username=username, password=password)
    return ssh

def execute_command(ssh, command):
    # Execute a command
    stdin, stdout, stderr = ssh.exec_command(command)
    # Print the output
    print(stdout.read().decode())
    # Print any errors
    print(stderr.read().decode())

def main():
    hostname = 'your_host'
    port = 22
    username = 'your_username'
    password = 'your_password'
    
    # Connect to the SSH server
    ssh = ssh_connect(hostname, port, username, password)
    
    # Execute a command
    execute_command(ssh, 'ls -l')
    
    # Close the connection
    ssh.close()

if __name__ == '__main__':
    main()