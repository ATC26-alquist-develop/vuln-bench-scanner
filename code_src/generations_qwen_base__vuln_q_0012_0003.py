import subprocess

def run_command(command):
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Return the output of the command
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If the command fails, return the error message
        return e.stderr

# Example usage
command = "ls -l"
output = run_command(command)
print(output)