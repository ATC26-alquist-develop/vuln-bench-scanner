import subprocess
import sys

def execute_command(command):
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Print the output and error messages
        print("Output:")
        print(result.stdout.decode())
        print("\nError:")
        print(result.stderr.decode())
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print(f"Error Output: {e.stderr.decode()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <command>")
        sys.exit(1)
    
    command = sys.argv[1]
    execute_command(command)