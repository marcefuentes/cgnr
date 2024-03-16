#! /usr/bin/env python

import logging
import os
import sys

import tools.colors as cc
from slurm.get_config import get_config
from slurm.tools import get_free_slots, not_submitted, submit_job

# Purpose: resubmit unfinished jobs
# Usage: python resubmit.py

queues = ["clk", "epyc"]

try:
    exe = get_config("exe")
except RuntimeError as e:
    print(f"{cc.red}{e}{cc.reset_format}")
    exit()
try:
    input_file_extension = get_config("input_file_extension")
except RuntimeError as e:
    print(f"{cc.red}{e}{cc.reset_format}")
    exit()
try:
    first_output_file_extension = get_config("first_output_file_extension")
except RuntimeError as e:
    print(f"{cc.red}{e}{cc.reset_format}")
    exit()
try:
    second_output_file_extension = get_config("second_output_file_extension")
except RuntimeError as e:
    print(f"{cc.red}{e}{cc.reset_format}")
    exit()
try:
    number_of_lines = get_config("number_of_lines")
except RuntimeError as e:
    print(f"{cc.red}{e}{cc.reset_format}")
    exit()

output_file_extensions = [first_output_file_extension, second_output_file_extension]

last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.log"
logging.basicConfig(filename=log_file,
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")

def get_jobs_to_submit():
    path = os.getcwd()
    mechanism = path.split("/")[-2]
    jobs_to_submit = []
    names = [name[:-4] for name in os.listdir() if name.endswith(input_file_extension)]
    for name in names:
        if not os.path.isfile(f"{name}{output_file_extensions[0]}"):
            if not_submitted(f"{mechanism}[0, 9]+", name):
                jobs_to_submit.append(int(name))
        else:
            with open(f"{name}{output_file_extensions[0]}") as f:
                if sum(1 for line in f) < number_of_lines and not_submitted(f"{mechanism}[0, 9]+", name):
                    jobs_to_submit.append(int(name))
    return jobs_to_submit

def remove_files(jobs_to_submit):
    for name in jobs_to_submit:
        for extension in output_file_extensions:
            if os.path.isfile(f"{name}{extension}"):
                os.remove(f"{name}{extension}")
            else:
                continue

def process_folder(queue, free_slots, jobs_to_submit, test=False):
    path = os.getcwd()
    path_folders = path.split("/")
    path_print = "/".join(path_folders[-3:])
    num_jobs_to_submit = min(free_slots, len(jobs_to_submit))
    job_array = ",".join(map(str, jobs_to_submit[:num_jobs_to_submit]))
    info = f"{path_print}/{job_array} to {queue}"
    last_job = job_array.split(",")[-1]
    job_name = f"{queue}-{path_folders[-2]}{last_job}"
    if test:
        print(f"Will submit {info}")
    else:
        return_code, stdout, stderr = submit_job(job_name, queue, job_array)
        if return_code != 0:
            print(f"{cc.red}sbatch command failed with return code {return_code}{cc.reset_format}")
            if stderr:
                print(stderr)
                logging.error(stderr)
            exit()
        else:
            for line in stdout.split("\n"):
                if line:
                    print(line)
                    logging.info(line)
        logging.info(info)
        print(f"{cc.green}{info}{cc.reset_format}")
    del jobs_to_submit[:num_jobs_to_submit]
    free_slots -= num_jobs_to_submit
    if len(jobs_to_submit) == 0:
        print(f"\n{cc.bold}{cc.green}All jobs submitted{cc.reset_format}")
        print(f"{cc.bold}{cc.cyan}{free_slots}{cc.reset_format} free slots in {cc.bold}{queue}{cc.reset_format}\n")
        exit()
    print(f"{cc.bold}{cc.red}{len(jobs_to_submit)}{cc.reset_format} jobs remain to be submitted")

    return jobs_to_submit

def main():

    test = len(sys.argv) > 1
    if test:
        print(f"\n{cc.bold}This is a test{cc.reset_format}")

    jobs_to_submit = get_jobs_to_submit()
    if len(jobs_to_submit) == 0:
        print(f"\n{cc.green}No jobs to submit. Exiting...{cc.reset_format}")
        return
    print(f"\n{cc.bold}{cc.cyan}{len(jobs_to_submit)}{cc.reset_format} jobs to submit")

    if test:
        print(f"\n{cc.bold}{cc.red}Will delete {output_file_extensions} of {jobs_to_submit}{cc.reset_format}")
    else:
        remove_files(jobs_to_submit)

    for queue in queues:
        free_slots = get_free_slots(queue)
        print(f"\n{cc.bold}{queue}:{cc.reset_format} {cc.cyan}{free_slots}{cc.reset_format} free slots")
        if test and not free_slots:
            free_slots = 100
        if free_slots:
            jobs_to_submit = process_folder(queue, free_slots, jobs_to_submit, test)

    print()

if __name__ == "__main__":
    main()
