#! /usr/bin/env python

import configparser
import os
import subprocess
import logging

# Purpose: browse through folders and submit jobs
# Usage: python submit.py

import mycolors as c
import myslots

queues = ["clk", "epyc"]
mail_user = "marcelinofuentes@gmail.com"
input_file_extension = ".glo"
output_file_extension = ".csv"

config_file_path = os.environ.get('CONFIG_FILE')
if not config_file_path:
  raise RuntimeError("CONFIG_FILE environment variable not set")

config = configparser.ConfigParser()
config.read(config_file_path)

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

def folder_list(path):
    folders = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folders.append(item_path)
    folders.sort()
    return folders

def get_job_min(path):
    job_min = 9999
    for file in os.listdir(path):
        if file.endswith(input_file_extension):
            basename = int(file.split(".")[0])
            if basename < job_min:
                job_min = basename
    return job_min

def get_job_max(path):
    job_max = 0
    for file in os.listdir(path):
        if file.endswith(input_file_extension):
            basename = int(file.split(".")[0])
            if basename > job_max:
                job_max = basename
    return job_max

def submit_jobs(free_slots):
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r") as f:
            given, last_job = f.read().strip().split(",")
        last_job = int(last_job)
    else:
        mechanisms = folder_list(os.getcwd())
        givens = folder_list(mechanisms[0])
        given = givens[0]
        given_folders = given.split("/")
        given_print = "/".join(given_folders[-3:])
        print(f"\n{c.bold}Submit jobs in {given_print}?{c.reset_format} "
              f"{yesno} ", end="")
        user_input = input()
        if user_input.lower() == "n":
            exit()
        last_job = 0
    os.chdir(given)
    job_max = get_job_max(given)
    if last_job == 0:
        job_min = get_job_min(given)
    else:
        job_min = last_job + 1
    given_folders = given.split("/")
    given_print = "/".join(given_folders[-3:])
    if os.path.isfile(os.path.join(given, f"{job_min}{output_file_extension}")):
        print(f"{c.red}{given_print}/{job_min}.csv already exists{c.reset_format}")
        exit()
    num_jobs_to_submit = min(free_slots, job_max - job_min + 1)
    last_job = job_min + num_jobs_to_submit - 1
    job_name = f"{queue}-{given_folders[-2]}{last_job}"
    job_time = f"{hours}:59:00"
    job_array = f"{job_min}-{last_job}"
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
    print(f"{c.green}{given_print}/{job_array}{c.reset_format}")
    logging.info(f"{given_print}/{job_array} to {queue}")
    free_slots -= num_jobs_to_submit
    if last_job == job_max:
        last_job = 0
        mechanism = os.path.dirname(given)
        givens = folder_list(mechanism)
        given_index = givens.index(given) + 1
        if given_index < len(givens):
            given = givens[given_index]
        else:
            mechanisms = folder_list(os.path.dirname(mechanism))
            mechanism_index = mechanisms.index(mechanism) + 1
            if mechanism_index < len(mechanisms):
                mechanism = mechanisms[mechanism_index]
                givens = folder_list(mechanism)
                given = givens[0]
            else:
                os.remove(last_job_file)
                print(f"{c.bold}{c.green}All jobs submitted{c.reset_format}")
                print(f"{c.cyan}{free_slots}{c.reset_format} free slots\n")
                exit()
    with open(last_job_file, "w") as f:
        f.write(f"{given},{last_job}")

    return free_slots

for queue in queues:
    max_submit = myslots.get_max_slots(queue, hours, "maxsubmit")
    max_running = myslots.get_max_slots(queue, hours, "maxjobspu")
    running_jobs = myslots.get_slots(queue, "RUNNING")
    pending_jobs = myslots.get_slots(queue, "PENDING")
    free_slots = max_submit - running_jobs - pending_jobs
    print(f"\n{queue}: {running_jobs} of {max_running} running, "
          f"{pending_jobs} pending, {c.cyan}{free_slots}{c.reset_format} free")
    while free_slots:
        free_slots = submit_jobs(free_slots)

print()

