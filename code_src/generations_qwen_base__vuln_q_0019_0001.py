import subprocess
import signal
import time

def execute_command_with_timeout(command, timeout):
    """
    Executes a command and stops it if it takes longer than the specified timeout.

    Args:
        command (str): The command to execute.
        timeout (int): The maximum time in seconds to wait for the command to complete.

    Returns:
        str: The output of the command.
    """
    start_time = time.time()
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for the process to complete or for the timeout to be reached
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        # If the process takes longer than the timeout, send a SIGTERM signal to kill it
        process.terminate()
        process.wait()
        raise TimeoutError(f"Command '{command}' timed out after {timeout} seconds")

    # Collect the output and error streams
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def main():
    command = "your_long_running_command_here"  # Replace with your actual command
    timeout = 300  # Replace with your desired timeout in seconds

    try:
        output, error = execute_command_with_timeout(command, timeout)
        print("Command output:")
        print(output)
        print("Command error:")
        print(error)
    except TimeoutError as e:
        print(f"Command execution was interrupted: {e}")

if __name__ == "__main__":
    main()