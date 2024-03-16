import subprocess

command = ["squeue", "-t", "RUNNING,PENDING", "-r", "-o", f"%j,%K | grep -E 'pi[0-9]+' | grep ,408"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout.decode("utf-8"))
