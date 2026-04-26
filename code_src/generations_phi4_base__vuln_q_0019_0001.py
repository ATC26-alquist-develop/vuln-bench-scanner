import subprocess
import time

def run_command_with_timeout(command, timeout):
    try:
        # Start the command as a subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        # Wait for the command to complete or timeout
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # If the command takes too long, terminate it
            process.kill()
            stdout, stderr = process.communicate()
            print("Command timed out and was killed.")
            return None, None

        return stdout, stderr

# Example usage:
command = "your_long_running_command_here"
timeout = 10  # Timeout in seconds

stdout, stderr = run_command_with_timeout(command, timeout)

if stdout is not None:
    print("Command output:", stdout.decode())
if stderr is not None:
    print("Command error output:", stderr.decode())