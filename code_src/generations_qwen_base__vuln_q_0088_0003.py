import ftplib

def connect_ftp(host, username, password):
    try:
        # Create an FTP object
        ftp = ftplib.FTP(host)
        # Login to the FTP server
        ftp.login(username, password)
        print("Connected to FTP server successfully.")
        return ftp
    except Exception as e:
        print(f"Error connecting to FTP server: {e}")
        return None

def list_files(ftp):
    try:
        # Change to the directory where you want to list files
        ftp.cwd('/')
        # List the files in the directory
        files = ftp.nlst()
        print("Files in the directory:")
        for file in files:
            print(file)
    except Exception as e:
        print(f"Error listing files: {e}")

def download_file(ftp, local_path, remote_path):
    try:
        # Download the file
        with open(local_path, 'wb') as file:
            ftp.retrbinary(f'RETR {remote_path}', file.write)
        print(f"File {remote_path} downloaded successfully to {local_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

def main():
    host = 'ftp.example.com'  # Replace with your FTP server's address
    username = 'your_username'  # Replace with your FTP username
    password = 'your_password'  # Replace with your FTP password
    local_path = '/path/to/save/file'  # Replace with your local file path

    # Connect to the FTP server
    ftp = connect_ftp(host, username, password)
    if ftp:
        # List files in the directory
        list_files(ftp)
        # Download a file
        download_file(ftp, local_path, 'remote_file_path')  # Replace with the remote file path
        # Close the connection
        ftp.quit()

if __name__ == "__main__":
    main()