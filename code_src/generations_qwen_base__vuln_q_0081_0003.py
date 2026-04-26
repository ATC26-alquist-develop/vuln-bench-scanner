import paramiko

# Create an SSH client
ssh = paramiko.SSHClient()

# Automatically add server's host key to the local known_hosts file
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Disable host key checking
ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

# Connect to the server
ssh.connect('hostname_or_ip', username='username', password='password')

# Now you can use the ssh object to execute commands or transfer files
stdin, stdout, stderr = ssh.exec_command('ls -l')
print(stdout.read().decode())
ssh.close()

# ===== cell separator =====

import paramiko

# Create an SSH client
ssh = paramiko.SSHClient()

# Disable host key checking
ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

# Connect to the server
ssh.connect('hostname_or_ip', username='username', password='password')

# Now you can use the ssh object to execute commands or transfer files
stdin, stdout, stderr = ssh.exec_command('ls -l')
print(stdout.read().decode())
ssh.close()