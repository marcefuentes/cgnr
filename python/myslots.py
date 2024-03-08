
import subprocess
import mycolors as c
from myget_config import get_config

def get_max_slots(queue, jobs):

    command = ["sacctmgr", "-p", "show", "qos", f"format=name,{jobs}"]
    output = subprocess.check_output(command)
    output = output.decode().strip().split("\n")
    qos_name = get_qos_name(queue)
    for line in output:
        if line.startswith(qos_name):
            fields = line.strip().split("|")
            slots = int(fields[1])
            break

    return slots

def get_slots(queue, state):

    command_squeue = ["squeue", "-t", state, "-r", "-o", "%j"]
    output_squeue = subprocess.Popen(command_squeue,
                                     stdout=subprocess.PIPE)
    command_grep = ["grep", "-E", f"^{queue}"]
    output_grep = subprocess.Popen(command_grep,
                                   stdin=output_squeue.stdout,
                                   stdout=subprocess.PIPE)
    command_wc = ["wc", "-l"]
    output_wc = subprocess.check_output(command_wc,
                                        stdin=output_grep.stdout)
    output = int(output_wc.decode().strip())

    return output

def get_free_slots(queue):

    max_submit = get_max_slots(queue, "maxsubmit")
    running_jobs = get_slots(queue, "RUNNING")
    pending_jobs = get_slots(queue, "PENDING")
    free_slots = max_submit - running_jobs - pending_jobs

    return free_slots
    
def get_qos_name(queue):

    try:
        hours = get_config("hours")
    except RuntimeError as e:
        print(f"{c.bold}{c.red}{e}{c.reset_format}")
        exit()

    command = ["sacctmgr", "-p", "show", "qos", "format=name,maxwall"]
    output = subprocess.check_output(command)
    output = output.decode().strip().split("\n")
    qos_name = f"{queue}_short"
    for line in output:
        if line.startswith(qos_name):
            fields = line.strip().split("|")
            maxwall = int(fields[1].split(":")[0])
            break
    if maxwall is None:
        print(f"{red}QOS {qos_name} not found{reset_format}")
        logging.error(f"QOS {qos_name} not found")
        exit()
    if hours >= maxwall:
        qos_name = f"{queue}_medium"

    return qos_name

