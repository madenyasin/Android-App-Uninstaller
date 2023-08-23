from subprocess import run
output = run("pwd", capture_output=True).stdout
print(output)
