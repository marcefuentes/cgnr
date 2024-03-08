
import os
import subprocess
from myget_config import get_config 

def submit_job(job_name, queue, job_array):

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

