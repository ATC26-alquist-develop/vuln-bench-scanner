import subprocess

def execute_command(command):
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully:")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the command:")
        print(e.stderr.decode())

if __name__ == "__main__":
    # Get command from user input
    user_input = input("Enter the command to execute: ")
    execute_command(user_input)