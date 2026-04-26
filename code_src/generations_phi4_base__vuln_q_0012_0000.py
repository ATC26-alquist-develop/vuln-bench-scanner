import subprocess

# Define the command and its arguments
command = "ls"
args = ["-l", "/home/user"]

# Run the command and capture the output
result = subprocess.run([command] + args, capture_output=True, text=True)

# Print the output
print(result.stdout)