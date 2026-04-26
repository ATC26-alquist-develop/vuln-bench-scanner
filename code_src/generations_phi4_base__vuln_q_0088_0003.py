from ftplib import FTP

# Replace these with your FTP server details
ftp_server = 'ftp.example.com'
username = 'your_username'
password = 'your_password'

# Establish a connection to the FTP server
ftp = FTP(ftp_server)

try:
    # Log in to the FTP server
    ftp.login(user=username, passwd=password)
    print("Logged in successfully.")

    # List the files in the current directory
    files = ftp.nlst()
    print("Files in the current directory:")
    for file in files:
        print(file)

    # Upload a file to the FTP server
    filename = 'local_file.txt'
    with open(filename, 'rb') as file:
        ftp.storbinary(f'STOR {filename}', file)
    print(f"Uploaded {filename} to the FTP server.")

    # Download a file from the FTP server
    remote_filename = 'remote_file.txt'
    with open(remote_filename, 'wb') as file:
        ftp.retrbinary(f'RETR {remote_filename}', file.write)
    print(f"Downloaded {remote_filename} from the FTP server.")

finally:
    # Close the connection
    ftp.quit()
    print("Connection closed.")