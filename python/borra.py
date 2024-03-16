import subprocess

# print the output of squeue RUNNING,PENDING jobs whose name (as retriebed by %j) contains "pi" followed by a number and 408 (as retrieved by %K)
subprocess.run(["squeue", "-o", "%j %K", "-s", "RUNNING,PENDING", "-u", "pi*408"], check=True)
```


