# Create a log file
log_file_path = 'example.log'
with open(log_file_path, 'w') as log_file:
    log_file.write("This is the initial content of the log file.\n")

# ===== cell separator =====

import os

# Change file permissions to allow all users to read and write
os.chmod(log_file_path, 0o666)

# ===== cell separator =====

# Write to the log file
with open(log_file_path, 'a') as log_file:
    log_file.write("This is a new entry in the log file.\n")

# ===== cell separator =====

# Read from the log file
with open(log_file_path, 'r') as log_file:
    content = log_file.read()
    print(content)

# ===== cell separator =====

import os

# Step 1: Create a log file
log_file_path = 'example.log'
with open(log_file_path, 'w') as log_file:
    log_file.write("This is the initial content of the log file.\n")

# Step 2: Change file permissions
os.chmod(log_file_path, 0o666)

# Step 3: Write to the log file
with open(log_file_path, 'a') as log_file:
    log_file.write("This is a new entry in the log file.\n")

# Step 4: Read from the log file
with open(log_file_path, 'r') as log_file:
    content = log_file.read()
    print(content)