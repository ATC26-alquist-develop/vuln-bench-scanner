import paramiko


   # Define the server's hostname, port, username, and password

   hostname = 'your_server_ip'

   port = 22  # Default SSH port

   username = 'your_username'

   password = 'your_password'


   # Create an SSH client instance

   ssh = paramiko.SSHClient()


   # Automatically add the server's host key (not recommended for production)

   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


   # Connect to the server

   try:

       ssh.connect(hostname, port, username, password)

       print("Connected to the server successfully.")

   except paramiko.AuthenticationException:

       print("Authentication failed, please verify your credentials.")

   except paramiko.SSHException as e:

       print(f"SSH connection error: {e}")

   except Exception as e:

       print(f"Error: {e}")

   finally:

       # Close the connection

       ssh.close()

# ===== cell separator =====

command = 'ls'  # Example command to list directory contents

   stdin, stdout, stderr = ssh.exec_command(command)


   # Read the command output

   print(stdout.read().decode())


   # Close the connection

   ssh.close()