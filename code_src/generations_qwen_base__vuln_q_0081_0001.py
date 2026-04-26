import paramiko

# Define the SFTP server details
hostname = 'your_sftp_server_ip_or_hostname'
port = 22  # Default SFTP port
username = 'your_username'
password = 'your_password'  # For simplicity, using password. Consider using SSH keys for security.
remote_path = '/path/to/remote/directory'
local_path = '/path/to/local/directory'

# Create an SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the SFTP server
ssh.connect(hostname, port, username, password)

# Create an SFTP session
sftp = ssh.open_sftp()

# Upload a file
local_file_path = '/path/to/local/file.txt'
remote_file_path = remote_path + '/file.txt'
sftp.put(local_file_path, remote_file_path)
print(f"File {local_file_path} uploaded to {remote_file_path}")

# Download a file
remote_file_to_download = remote_path + '/file.txt'
local_file_to_download = local_path + '/file_downloaded.txt'
sftp.get(remote_file_to_download, local_file_to_download)
print(f"File {remote_file_to_download} downloaded to {local_file_to_download}")

# Close the SFTP session and the SSH connection
sftp.close()
ssh.close()