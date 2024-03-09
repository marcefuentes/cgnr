#! /usr/bin/env python

import logging
import os
import sys

import mycolors as c
from myget_config import get_config
import myslurm

# Purpose: resubmit unfinished jobs
# Usage: python resubmit.py

queues = ["clk", "epyc"]

try:
    exe = get_config("exe")
except RuntimeError as e:
    print(f"{c.red}{e}{c.reset_format}")
    exit()
try:
    input_file_extension = get_config("input_file_extension")
except RuntimeError as e:
    print(f"{c.red}{e}{c.reset_format}")
    exit()
try:
    first_output_file_extension = get_config("first_output_file_extension")
except RuntimeError as e:
    print(f"{c.red}{e}{c.reset_format}")
    exit()
try:
    second_output_file_extension = get_config("second_output_file_extension")
except RuntimeError as e:
    print(f"{c.red}{e}{c.reset_format}")
    exit()
try:
    number_of_lines = get_config("number_of_lines")
except RuntimeError as e:
    print(f"{c.red}{e}{c.reset_format}")
    exit()

output_file_extensions = [first_output_file_extension, second_output_file_extension]

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
        return_code, stdout, stderr = myslurm.submit_job(job_name, queue, job_array)
        if return_code != 0:
            print(f"{c.red}sbatch command failed with return code {return_code}{c.reset_format}")
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
        print(f"{c.green}{info}{c.reset_format}")
    del jobs_to_submit[:num_jobs_to_submit]
    free_slots -= num_jobs_to_submit
    if len(jobs_to_submit) == 0:
        print(f"\n{c.bold}{c.green}All jobs submitted{c.reset_format}")
        print(f"{c.bold}{c.cyan}{free_slots}{c.reset_format} free slots in {c.bold}{queue}{c.reset_format}\n")
        exit()
    print(f"{c.bold}{c.red}{len(jobs_to_submit)}{c.reset_format} jobs remain to be submitted")

    return jobs_to_submit

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
        free_slots = myslurm.get_free_slots(queue)
        print(f"\n{c.bold}{queue}:{c.reset_format} {c.cyan}{free_slots}{c.reset_format} free slots")
        if test and not free_slots:
            free_slots = 100
        if free_slots:
            jobs_to_submit = process_folder(queue, free_slots, jobs_to_submit, test)

    print()

if __name__ == "__main__":
    main()
