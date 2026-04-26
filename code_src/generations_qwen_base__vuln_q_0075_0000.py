import os

# Define the command you want to execute
command = "ls -l"

# Use os.popen() to execute the command
# The command is passed as a string
# os.popen() returns a file-like object
# You can read from this object to get the output of the command
with os.popen(command) as popen_obj:
    # Read the output of the command
    output = popen_obj.read()
    # Print the output
    print(output)

# ===== cell separator =====

import subprocess

# Define the command you want to execute
command = "ls -l"

# Use subprocess to execute the command
# subprocess.run() returns a subprocess.CompletedProcess object
# You can access the output and return code of the command
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Print the output and return code
print("Output:", result.stdout)
print("Return Code:", result.returncode)