import subprocess

# The command you want to run
command = ["ls", "-l"]  # This is a Unix command to list files in long format

# Run the command and capture the output
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command was successful
if result.returncode == 0:
    # Print the standard output
    print("Command output:")
    print(result.stdout)
else:
    # Print the standard error
    print("Command error:")
    print(result.stderr)

# ===== cell separator =====

import subprocess

# The command you want to run, with shell=True
command = "ls -l *"  # This will list all files in the current directory

# Run the command and capture the output
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command was successful
if result.returncode == 0:
    # Print the standard output
    print("Command output:")
    print(result.stdout)
else:
    # Print the standard error
    print("Command error:")
    print(result.stderr)