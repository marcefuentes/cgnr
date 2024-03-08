#! /usr/bin/env python

import configparser
import logging
import os
import subprocess
import sys

import mycolors as c
from mylist_of_folders import list_of_folders
from mysubmit_job import submit_job
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

def process_folder(queue, free_slots, last_job, test):
    path = os.getcwd()
    path_folders = path.split("/")
    path_print = "/".join(path_folders[-3:])
    job_max = get_job_max(path)
    if last_job == 0:
        job_min = get_job_min(path)
    else:
        job_min = last_job + 1
    if os.path.isfile(os.path.join(path, f"{job_min}{output_file_extension}")):
        print(f"{c.red}{path_print}/{job_min}{output_file_extension} already exists{c.reset_format}")
        last_job = 0
        return free_slots, last_job
    num_jobs_to_submit = min(free_slots, job_max - job_min + 1)
    last_job = job_min + num_jobs_to_submit - 1
    job_name = f"{queue}-{path_folders[-2]}{last_job}"
    job_array = f"{job_min}-{last_job}"
    info = f"{path_print}/{job_array} to {queue}"
    if test:
        print(f"Will submit {info}")
    else:
        try:
            return_code, stdout, stderr = submit_job(job_name, queue, job_array)
        except RuntimeError as e:
            print(f"{c.red}Error: {e}{c.reset_format}")
            exit()
        if return_code != 0:
            print(f"{c.red}Error: command failed with return code {return_code}{c.reset_format}")
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
    free_slots -= num_jobs_to_submit
    if last_job == job_max:
        last_job = 0
    return free_slots, last_job

def process_variant(queue, free_slots, test=False):
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r") as f:
            path, last_job = f.read().strip().split(",")
        last_job = int(last_job)
    else:
        mechanisms = list_of_folders(os.getcwd())
        givens = list_of_folders(mechanisms[0])
        path = givens[0]
        path_folders = path.split("/")
        path_print = "/".join(path_folders[-3:])
        print(f"\n{c.bold}Submit jobs in {path_print}?{c.reset_format} "
              f"{c.yesno} ", end="")
        user_input = input()
        if user_input.lower() == "n":
            exit()
        last_job = 0
    os.chdir(path)
    free_slots, last_job = process_folder(queue, free_slots, last_job, test)

    if last_job == 0: 
        mechanism = os.path.dirname(path)
        givens = list_of_folders(mechanism)
        given_index = givens.index(given) + 1
        if given_index < len(givens):
            path = givens[given_index]
        else:
            mechanisms = list_of_folders(os.path.dirname(mechanism))
            mechanism_index = mechanisms.index(mechanism) + 1
            if mechanism_index < len(mechanisms):
                mechanism = mechanisms[mechanism_index]
                givens = list_of_folders(mechanism)
                path = givens[0]
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
            f.write(f"{path},{last_job}")

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
            free_slots = process_variant(queue, free_slots, test)

    print()

if __name__ == "__main__":
    main()
