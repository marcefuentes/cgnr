
import os
import subprocess
from myget_config import get_config 

def submit_job(job_name, queue, job_array):

    exe = get_config("exe")
    hours = get_config("hours")
    memory = get_config("memory")
    mail_user = get_config("mail_user")

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

