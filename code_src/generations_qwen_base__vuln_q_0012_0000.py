import subprocess

# Define the command you want to run
command = ['ls', '-l']

# Run the command and capture the output
try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Command output:")
    print(result.stdout)
    print("Command error:")
    print(result.stderr)
except subprocess.CalledProcessError as e:
    print(f"Command execution failed with return code {e.returncode}")
    print(f"Error output: {e.stderr}")

# ===== cell separator =====

command = ['git', 'status']

# ===== cell separator =====

command = ['git', 'status', '--short']