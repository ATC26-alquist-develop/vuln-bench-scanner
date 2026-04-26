import paramiko

def sftp_upload(host, port, username, password, local_file, remote_file):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        ssh.connect(host, port=port, username=username, password=password)

        # Create an SFTP client from the SSH connection
        sftp = ssh.open_sftp()

        # Upload the file
        sftp.put(local_file, remote_file)

        # Close the SFTP connection
        sftp.close()

        # Close the SSH connection
        ssh.close()

        print(f"File {local_file} uploaded to {remote_file} successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
sftp_upload('sftp.example.com', 22, 'username', 'password', 'local_file.txt', 'remote_file.txt')