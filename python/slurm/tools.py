
import re
import subprocess
import tools.colors as cc
from slurm.get_config import get_config

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

def get_slots(key, state):
    command = f"squeue -t {state} -r -o %f | grep -E {key} | wc -l"
    output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    output = int(output)
    return output

def get_free_slots(queue):
    max_submit = get_max_slots(queue, "maxsubmit")
    running_jobs = get_slots(queue, "RUNNING")
    pending_jobs = get_slots(queue, "PENDING")
    free_slots = max_submit - running_jobs - pending_jobs
    return free_slots

def submitted_job(mechanism, job_name):
    command = f"squeue -t RUNNING,PENDING -r -o %j,%K | grep {mechanism}, {job_name}"
    try:
        subprocess.check_output(f"{command} >/dev/null 2>&1", shell=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

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
    job_name = f"{mechanism}_{last_job}"
    job_time = f"{hours}:59:00"

    command = ["sbatch",
               "--job-name", job_name,
               "--output=%a_slurm.out",
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

