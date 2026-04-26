import subprocess
import shlex

def execute_command(command):
    # Use shlex.split to properly handle command arguments
    args = shlex.split(command)
    
    # Use subprocess.run with shell=False for security
    result = subprocess.run(args, capture_output=True, text=True, shell=False)
    
    return result.stdout