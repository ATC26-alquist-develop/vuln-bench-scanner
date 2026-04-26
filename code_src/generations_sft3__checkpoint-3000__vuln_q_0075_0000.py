import subprocess

def run_command(command):
    try:
        # Run command with shell=False for security
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=False  # Crucial security setting
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        return None

# ===== cell separator =====

import subprocess

def run_command_windows(command):
    try:
        # Run command with shell=False for security
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=False  # Crucial security setting
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        return None