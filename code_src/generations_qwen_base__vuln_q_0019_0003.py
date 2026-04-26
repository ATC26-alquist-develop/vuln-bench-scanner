import subprocess
import signal
import time

def run_command_with_timeout(command, timeout):
    """
    Runs a shell command and terminates it if it doesn't finish within the specified timeout.

    :param command: The shell command to run.
    :param timeout: The maximum time in seconds to wait for the command to complete.
    :return: The output of the command as a string.
    """
    start_time = time.time()
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for the process to finish or timeout
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        # Send a SIGTERM signal to terminate the process
        process.terminate()
        process.wait()
        raise TimeoutError(f"Command '{command}' timed out after {timeout} seconds.")

    # Collect the output and error
    output, error = process.communicate()
    output = output.decode('utf-8')
    error = error.decode('utf-8')

    return output, error

# Example usage:
command = "sleep 5"
timeout = 3

try:
    output, error = run_command_with_timeout(command, timeout)
    print("Output:")
    print(output)
    print("Error:")
    print(error)
except TimeoutError as e:
    print(e)