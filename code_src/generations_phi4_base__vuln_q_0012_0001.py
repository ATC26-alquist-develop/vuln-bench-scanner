import subprocess

# The command you want to execute
command = "ls"  # For example, this command lists directory contents on Unix-like systems

# Execute the command
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command was successful
if result.returncode == 0:
    print("Command executed successfully")
    print("Output:")
    print(result.stdout)
else:
    print("Command failed")
    print("Error:")
    print(result.stderr)