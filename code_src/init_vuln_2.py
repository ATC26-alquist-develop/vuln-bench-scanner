import subprocess
def shell_exec(user_input):
    subprocess.call(user_input, shell=True)
shell_exec(input())
