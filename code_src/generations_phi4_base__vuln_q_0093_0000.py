import os

# Execute a system command and read its output
output = os.popen('ls -l').read()

print(output)

# ===== cell separator =====

import subprocess

# Execute a system command and read its output
output = subprocess.check_output('ls -l', shell=True)

print(output)