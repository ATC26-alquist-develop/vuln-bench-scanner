import os
from pathlib import Path

# Create a log file
log_file = Path("log.txt")

# Check if the log file already exists
if not log_file.exists():
    log_file.touch()

# Set the permissions of the log file
os.chmod(log_file, 0o777)

# Read and write to the log file
with open(log_file, "a") as f:
    f.write("This is a log entry.\n")