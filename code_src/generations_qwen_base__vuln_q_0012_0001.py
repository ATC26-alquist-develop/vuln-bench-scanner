import subprocess

def execute_command(command):
    """
    Executes a system command and returns the output.

    :param command: The command to execute as a list (e.g., ['ls', '-l'])
    :return: The output of the command as a string
    """
    try:
        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If the command fails, return the error message
        return f"Error: {e.stderr}"

# Example usage
command = ['ls', '-l']
output = execute_command(command)
print(output)