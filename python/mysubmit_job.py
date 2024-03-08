
import configparser
import os

def submit_job(job_name, queue, job_array):

    config_file_path = os.environ.get('CONFIG_FILE')
    if not config_file_path:
      return RuntimeError("CONFIG_FILE environment variable not set")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    exe = config.get("DEFAULT", "exe")
    hours = config.getint("DEFAULT", "hours")
    memory = config.get("DEFAULT", "memory")
    mail_user = config.get("DEFAULT", "mail_user")

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

