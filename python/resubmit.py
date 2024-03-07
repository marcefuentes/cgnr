#! /usr/bin/env python

import configparser
import os
import subprocess
import logging

# Purpose: resubmit unfinished jobs
# Usage: python resubmit.py

import mycolors as c
import myslots

queues = ["clk", "epyc"]
mail_user = "marcelinofuentes@gmail.com"
input_file_extension = ".glo"
output_file_extensions = [".csv", ".frq"]

config = configparser.ConfigParser()
config.read("submit.ini")

exe = config.get("DEFAULT", "exe")
default_lines = config.getint("DEFAULT", "number_of_lines")
default_hours = config.getint("DEFAULT", "hours")
default_memory = config.get("DEFAULT", "memory")

if exe == "dgnr":
    number_of_lines = config.getint("dgnr", "number_of_lines")
    hours = config.getint("dgnr", "hours")
    memory = config.get("dgnr", "memory")
else:
    number_of_lines = default_lines
    hours = default_hours
    memory = default_memory

executable = f"/home/ulc/ba/mfu/code/{exe}/bin/{exe}"
last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.log"
logging.basicConfig(filename=log_file,
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")
yesno = f"[{c.bold}{c.green}Yes{c.reset_format}/{c.bold}{c.red}No{c.reset_format}]"

def submit_jobs(free_slots, jobs_to_submit):
    num_jobs_to_submit = min(free_slots, len(jobs_to_submit))
    job_array = ",".join(map(str, jobs_to_submit[:num_jobs_to_submit]))
    print(f"\n{c.bold}Submit {job_array}?{c.reset_format} "
          f"{yesno} ", end="")
    user_input = input()
    if user_input.lower() == "n":
        exit()
    last_job = job_array.split(",")[-1]
    job_name = f"{queue}-{last_job}"
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
    output = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    output = output.stdout.strip()
    print(output)
    logging.info(output)
    logging.info(f"{given_print}/{jobs_to_submit[0]}-{jobs_to_submit[num_jobs_to_submit - 1]} to {queue}")
    del jobs_to_submit[:num_jobs_to_submit]
    free_slots -= num_jobs_to_submit 

    return free_slots, jobs_to_submit

names = [name[:-4] for name in os.listdir() if name.endswith(input_file_extension)]
jobs_to_submit = []
for name in names:
    if not os.path.isfile(f"{name}{output_file_extensions[0]}"):
        jobs_to_submit.append(int(name))
    else:
        with open(f"{name}{output_file_extensions[0]}") as f:
            if sum(1 for line in f) < number_of_lines:
                jobs_to_submit.append(int(name))

print(f"\n{c.bold}Delete {output_file_extensions} of {jobs_to_submit}?{c.reset_format} "
      f"{yesno} ", end="")
user_input = input()
if user_input.lower() == "n":
    exit()
for name in jobs_to_submit:
    for extension in output_file_extensions:
        if os.path.isfile(f"{name}{extension}"):
            os.remove(f"{name}{extension}")
        else:
            continue

given = os.getcwd()
given_folders = given.split("/")
given_print = "/".join(given_folders[-3:])

for queue in queues:
    max_submit = myslots.get_max_slots(queue, hours, "maxsubmit")
    max_running = myslots.get_max_slots(queue, hours, "maxjobspu")
    running_jobs = myslots.get_slots(queue, "RUNNING")
    pending_jobs = myslots.get_slots(queue, "PENDING")
    free_slots = max_submit - running_jobs - pending_jobs
    print(f"\n{queue}: {running_jobs} of {max_running} running, "
          f"{pending_jobs} pending, {c.cyan}{free_slots}{c.reset_format} free")
    if free_slots > 0 and len(jobs_to_submit) > 0:
        free_slots, jobs_to_submit = submit_jobs(free_slots, jobs_to_submit)

    print(f"{c.red}{len(jobs_to_submit)} jobs remain to be submitted{c.reset_format}")
    print(f"{c.cyan}{free_slots}{c.reset_format} free slots")
    if len(jobs_to_submit) == 0:
        break

print()

