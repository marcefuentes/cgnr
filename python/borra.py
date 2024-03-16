import subprocess

command = ["squeue", "-t", "RUNNING,PENDING", "-r", "-o", f"%j,%K | grep -E 'pi[0-9]+' | grep ,408"]
# print the output of squeue filetered by "pi" followed by a number and 408
subprocess.run(command)


