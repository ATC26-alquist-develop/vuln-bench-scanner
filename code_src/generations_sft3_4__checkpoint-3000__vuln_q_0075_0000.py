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
import shlex

def run_command(command):
    try:
        # Safely parse command arguments
        cmd_parts = shlex.split(command)
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            check=True,
            shell=False  # Crucial security setting
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        return None