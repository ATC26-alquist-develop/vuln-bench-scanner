import subprocess

# Define the command to be executed
command = "ls -l"

# Use subprocess.run to execute the command and capture the output
process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command was successful
if process.returncode == 0:
    # Print the output
    print("Command output:")
    print(process.stdout)
else:
    # Print the error message
    print("Error:", process.stderr)