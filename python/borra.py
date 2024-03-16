import subprocess

command = ["squeue", "-t", "RUNNING,PENDING", "-r", "-o", f"%j,%K | grep -E 'pi[0-9]+' | grep ,408"]
out
