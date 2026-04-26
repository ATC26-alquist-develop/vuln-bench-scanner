import subprocess
import threading

def run_command_with_timeout(command, timeout):
    """
    Runs a shell command with a specified timeout.

    :param command: The shell command to run as a list of arguments.
    :param timeout: The time limit in seconds for the command to complete.
    :return: The return code of the command.
    """
    def target():
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")

    # Create a thread to run the command
    thread = threading.Thread(target=target)
    thread.start()

    # Wait for the thread to complete or timeout
    thread.join(timeout)

    # If the thread is still alive, it means the command timed out
    if thread.is_alive():
        print(f"Command timed out after {timeout} seconds.")
        thread.join()  # Ensure the thread is cleaned up
        return -1  # Return a non-zero value to indicate a timeout

    # If the thread has finished, return the command's return code
    return thread.exitcode

# Example usage:
if __name__ == "__main__":
    command = ["sleep", "5"]  # Replace with your command
    timeout = 3  # Replace with your desired timeout in seconds
    return_code = run_command_with_timeout(command, timeout)
    if return_code == -1:
        print("Command did not finish within the time limit.")
    else:
        print(f"Command finished with return code {return_code}.")