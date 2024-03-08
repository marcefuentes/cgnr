#! /usr/bin/env python

import configparser
import logging
import os
import subprocess
import sys

import mycolors as c
from mylist_of_folders import list_of_folders
import myslots

# Purpose: browse through folders and submit jobs
# Usage: python submit.py or python submit.py test

queues = ["clk", "epyc"]

config_file_path = os.environ.get('CONFIG_FILE')
if not config_file_path:
  raise RuntimeError("CONFIG_FILE environment variable not set")

config = configparser.ConfigParser()
config.read(config_file_path)

exe = config.get("DEFAULT", "exe")
hours = config.getint("DEFAULT", "hours")
memory = config.get("DEFAULT", "memory")
executable = f"/home/ulc/ba/mfu/code/{exe}/bin/{exe}"
mail_user = config.get("DEFAULT", "mail_user")

input_file_extension = config.get("DEFAULT", "input_file_extension")
output_file_extension = config.get("DEFAULT", "first_output_file_extension")

last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.log"
logging.basicConfig(filename=log_file,
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")

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

def submit_job(command):
    output = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    output = output.stdout.strip()
    print(output)
    logging.info(output)

def process_folders(queue, free_slots, test=False):
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r") as f:
            given, last_job = f.read().strip().split(",")
        last_job = int(last_job)
    else:
        mechanisms = list_of_folders(os.getcwd())
        givens = list_of_folders(mechanisms[0])
        given = givens[0]
    given_folders = given.split("/")
    given_print = "/".join(given_folders[-3:])
    if not os.path.isfile(last_job_file):
        print(f"\n{c.bold}Submit jobs in {given_print}?{c.reset_format} "
              f"{c.yesno} ", end="")
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
    if os.path.isfile(os.path.join(given, f"{job_min}{output_file_extension}")):
        print(f"{c.red}{given_print}/{job_min}{output_file_extension} already exists{c.reset_format}")
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
    info = f"{given_print}/{job_array} to {queue}"
    if test:
        print(f"Will submit {info}")
    else:
        submit_job(command)
        logging.info(info)
        print(f"{c.green}{info}{c.reset_format}")
    free_slots -= num_jobs_to_submit
    if last_job == job_max:
        last_job = 0
        mechanism = os.path.dirname(given)
        givens = list_of_folders(mechanism)
        given_index = givens.index(given) + 1
        if given_index < len(givens):
            given = givens[given_index]
        else:
            mechanisms = list_of_folders(os.path.dirname(mechanism))
            mechanism_index = mechanisms.index(mechanism) + 1
            if mechanism_index < len(mechanisms):
                mechanism = mechanisms[mechanism_index]
                givens = list_of_folders(mechanism)
                given = givens[0]
            else:
                if test:
                    print(f"Will remove last_job_file")
                else:
                    os.remove(last_job_file)
                print(f"{c.bold}{c.green}All jobs submitted{c.reset_format}")
                print(f"{c.cyan}{free_slots}{c.reset_format} free slots in {c.bold}{queue}{c.reset_format}\n")
                exit()
    if test:
        print(f"Will write {last_job} to last_job_file")
    else:
        with open(last_job_file, "w") as f:
            f.write(f"{given},{last_job}")

    return free_slots

def main():

    test = len(sys.argv) > 1
    if test:
        print(f"\n{c.bold}This is a test{c.reset_format}")

    for queue in queues:
        max_submit = myslots.get_max_slots(queue, hours, "maxsubmit")
        max_running = myslots.get_max_slots(queue, hours, "maxjobspu")
        running_jobs = myslots.get_slots(queue, "RUNNING")
        pending_jobs = myslots.get_slots(queue, "PENDING")
        free_slots = max_submit - running_jobs - pending_jobs
        if test and not free_slots:
            free_slots = 100
        print(f"\n{c.bold}{queue}{c.reset_format}: {running_jobs} of {max_running} running, "
              f"{pending_jobs} pending, {c.cyan}{free_slots}{c.reset_format} free")
        while free_slots:
            free_slots = process_folders(queue, free_slots, test)

    print()

if __name__ == "__main__":
    main()
