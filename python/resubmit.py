#! /usr/bin/env python

import configparser
import logging
import os
import subprocess
import sys

import mycolors as c
import myslots

# Purpose: resubmit unfinished jobs
# Usage: python resubmit.py

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
output_file_extensions = [config.get("DEFAULT", "first_output_file_extension"),
                          config.get("DEFAULT", "second_output_file_extension")]
number_of_lines = config.getint("DEFAULT", "number_of_lines")

last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.log"
logging.basicConfig(filename=log_file,
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")

def get_jobs_to_submit():
    jobs_to_submit = []
    names = [name[:-4] for name in os.listdir() if name.endswith(input_file_extension)]
    for name in names:
        if not os.path.isfile(f"{name}{output_file_extensions[0]}"):
            jobs_to_submit.append(int(name))
        else:
            with open(f"{name}{output_file_extensions[0]}") as f:
                if sum(1 for line in f) < number_of_lines:
                    jobs_to_submit.append(int(name))
    return jobs_to_submit

def remove_files(jobs_to_submit):
    for name in jobs_to_submit:
        for extension in output_file_extensions:
            if os.path.isfile(f"{name}{extension}"):
                os.remove(f"{name}{extension}")
            else:
                continue

def submit_job(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        print(stderr)
        logging.error(stderr)
        exit()
    else:
        print(stdout)
        logging.info(stdout)

def process_folder(queue, free_slots, jobs_to_submit, test=False):
    path = os.getcwd()
    path_folders = path.split("/")
    path_print = "/".join(path_folders[-3:])
    num_jobs_to_submit = min(free_slots, len(jobs_to_submit))
    job_array = ",".join(map(str, jobs_to_submit[:num_jobs_to_submit]))
    last_job = job_array.split(",")[-1]
    job_name = f"{queue}-{path_folders[-2]}{last_job}"
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
    info = f"{path_print}/{jobs_to_submit[0]}-{jobs_to_submit[num_jobs_to_submit - 1]} to {queue}"
    if test:
        print(f"Will submit {info}")
    else:
        submit_job(command)
        logging.info(info)
        print(f"{c.green}{info}{c.reset_format}")
    del jobs_to_submit[:num_jobs_to_submit]
    free_slots -= num_jobs_to_submit 

    return free_slots, jobs_to_submit

def main():

    test = len(sys.argv) > 1
    if test:
        print(f"\n{c.bold}This is a test{c.reset_format}")

    jobs_to_submit = get_jobs_to_submit()
    if len(jobs_to_submit) == 0:
        print(f"\n{c.green}No jobs to submit. Exiting...{c.reset_format}")
        return
    print(f"\n{c.bold}{c.cyan}{len(jobs_to_submit)}{c.reset_format} jobs to submit")

    if test:
        print(f"\n{c.bold}{c.red}Will delete {output_file_extensions} of {jobs_to_submit}{c.reset_format}")
    else:
        remove_files(jobs_to_submit)

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
        if free_slots and len(jobs_to_submit):
            free_slots, jobs_to_submit = process_folder(queue, free_slots, jobs_to_submit, test)

        if len(jobs_to_submit) == 0:
            print(f"\n{c.bold}{c.green}All jobs submitted{c.reset_format}")
            print(f"{c.bold}{c.cyan}{free_slots}{c.reset_format} free slots in {c.bold}{queue}{c.reset_format}")
            return
        else:
            print(f"{c.bold}{c.red}{len(jobs_to_submit)}{c.reset_format} jobs remain to be submitted")

    print()

if __name__ == "__main__":
    main()
