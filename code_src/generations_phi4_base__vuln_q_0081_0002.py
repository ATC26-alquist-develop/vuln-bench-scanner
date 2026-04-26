import paramiko

# ===== cell separator =====

ssh = paramiko.SSHClient()

# ===== cell separator =====

ssh.load_system_host_keys()

# ===== cell separator =====

ssh.connect(hostname='your-ssh-server.com', port=22, username='your-username', password='your-password')

# ===== cell separator =====

stdin, stdout, stderr = ssh.exec_command('your-command')

# ===== cell separator =====

output = stdout.readlines()
   error = stderr.readlines()

# ===== cell separator =====

ssh.close()

# ===== cell separator =====

import paramiko

# Create an SSH client instance
ssh = paramiko.SSHClient()

# Load the system's known hosts (optional but recommended for security)
ssh.load_system_host_keys()

# Connect to the remote server
ssh.connect(hostname='your-ssh-server.com', port=22, username='your-username', password='your-password')

# Execute a command on the remote server
stdin, stdout, stderr = ssh.exec_command('your-command')

# Read the command output
output = stdout.readlines()
error = stderr.readlines()

# Print the output and error streams
print('Output:')
for line in output:
    print(line.strip())

print('Error:')
for line in error:
    print(line.strip())

# Close the SSH connection
ssh.close()