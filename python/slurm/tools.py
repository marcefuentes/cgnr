
import re
import subprocess
import tools.colors as cc
from slurm.get_config import get_config

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

def submitted_job(mechanism, job_name):
    command = ["squeue", "-t", "RUNNING,PENDING", "-r", "-o", "%j,%K"]
    output = subprocess.check_output(command, text=True).strip().split("\n")
    for line in output:
        for i in range(1, 6):
            if f"{mechanism}{i}" in line and f",{job_name}" in line:
                return True
        if f"{mechanism}-" in line and f",{job_name}" in line: 
            return True
    return False

def get_slots(key, state):

    command_squeue = ["squeue", "-t", state, "-r", "-o", "%j"]
    output_squeue = subprocess.Popen(command_squeue,
                                     stdout=subprocess.PIPE)
    command_grep = ["grep", "-E", f"{key}"]
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
        print(f"{cc.bold}{cc.red}{e}{cc.reset_format}")
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

def submit_job(mechanism, last_job, queue, job_array):

    try: 
        exe = get_config("exe")
    except RuntimeError as e:
        return -1, None, e
    try:
        hours = get_config("hours")
    except RuntimeError as e:
        return -1, None, e
    try:
        memory = get_config("memory")
    except RuntimeError as e:
        return -1, None, e
    try:
        mail_user = get_config("mail_user")
    except RuntimeError as e:
        return -1, None, e

    executable = f"/home/ulc/ba/mfu/code/{exe}/bin/{exe}"
    job_name = f"{mechanism}-{last_job}-{queue}"
    job_time = f"{hours}:59:00"

    command = ["sbatch",
               "--job-name", job_name,
               "--output", f"{job_name}.%j.out",
               "--constraint", queue,
               "--nodes=1",
               "--tasks=1",
               "--time", job_time,
               "--mem", memory,
               "--mail-type=begin,end",
               "--mail-user", mail_user,
               "--array", job_array,
               "--wrap", f"srun {executable} ${{SLURM_ARRAY_TASK_ID}}"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr

