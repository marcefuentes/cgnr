#!/usr/bin/env python

""" Submit jobs. """

import os
import sys

import common_modules.color
from common_modules.get_config import get_config
from modules.argparse_utils import parse_args
from modules.list_of_folders import list_of_folders
from modules.process_jobs import process_jobs
import modules.slurm_tools as st

# Purpose: browse through folders and submit jobs
# Usage: python submit.py or python submit.py test

def get_job_min(current_path):
    """ Get the minimum job number in the current folder. """
    input_file_extension = get_config("input_file_extension")
    job_min = 9999
    for file in os.listdir(current_path):
        if file.endswith(input_file_extension):
            basename = int(file.split(".")[0])
            job_min = min(job_min, basename)
    return job_min

def get_job_max(current_path):
    """ Get the maximum job number in the current folder. """
    input_file_extension = get_config("input_file_extension")
    job_max = 0
    for file in os.listdir(current_path):
        if file.endswith(input_file_extension):
            basename = int(file.split(".")[0])
            job_max = max(job_max, basename)
    return job_max

def process_folder(constraint, free_slots, last_job, test):
    """ Submit jobs in the current folder """
    output_file_extension, *_ = get_config("output_file_extensions")
    current_path = os.getcwd()
    current_path_folders = current_path.split("/")
    current_path_print = "/".join(current_path_folders[-3:])
    if last_job == 0:
        job_min = get_job_min(current_path)
    else:
        job_min = last_job + 1
    if os.path.isfile(os.path.join(current_path, f"{job_min}{output_file_extension}")):
        msg = (
            f"{color.RED}{current_path_print}/{job_min}{output_file_extension} "
            f"already exists.{color.RESET}"
        )
        print(msg)
        last_job = 0
        return free_slots, last_job
    job_max = get_job_max(current_path)
    num_jobs_to_submit = min(free_slots, job_max - job_min + 1)
    last_job = job_min + num_jobs_to_submit - 1
    job_array_string = f"{job_min}-{last_job}"
    process_jobs(current_path, job_array_string, constraint, test)
    free_slots -= num_jobs_to_submit
    if last_job == job_max:
        last_job = 0
    return free_slots, last_job

def process_variant(constraint, free_slots, test, last_job_file):
    """ Process the parent directory. """
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r", encoding="utf-8") as f:
            current_path, last_job = f.read().strip().split(",")
        last_job = int(last_job)
    else:
        if test:
            print("Submission is about to start in a new variant. Cannot run with --test option.")
            sys.exit()
        mechanisms = list_of_folders(os.getcwd())
        givens = list_of_folders(mechanisms[0])
        current_path = givens[0]
        current_path_folders = current_path.split("/")
        current_path_print = "/".join(current_path_folders[-3:])
        print(f"\n{color.BOLD}Submit jobs in {current_path_print}?{color.RESET} {color.YESNO} ", end="")
        user_input = input()
        if user_input.lower() == "n":
            sys.exit()
        last_job = 0
    os.chdir(current_path)
    free_slots, last_job = process_folder(constraint, free_slots, last_job, test)

    if last_job == 0:
        mechanism = os.path.dirname(current_path)
        givens = list_of_folders(mechanism)
        given_index = givens.index(current_path) + 1
        if given_index < len(givens):
            current_path = givens[given_index]
        else:
            mechanisms = list_of_folders(os.path.dirname(mechanism))
            mechanism_index = mechanisms.index(mechanism) + 1
            if mechanism_index < len(mechanisms):
                mechanism = mechanisms[mechanism_index]
                givens = list_of_folders(mechanism)
                current_path = givens[0]
            else:
                if test:
                    print(f"Would remove {last_job_file}.{color.RESET}")
                else:
                    os.remove(last_job_file)
                print(f"{color.BOLD}{color.GREEN}All jobs submitted.{color.RESET}")
                msg = (
                    f"{color.BOLD}{color.CYAN}{free_slots}{color.RESET} "
                    f"free slots in {color.BOLD}{constraint}{color.RESET}.\n"
                )
                print(msg)
                sys.exit()
    if test:
        print(f"Would write {current_path},{last_job} to {last_job_file}.{color.RESET}")
    else:
        with open(last_job_file, "w", encoding="utf-8") as f:
            f.write(f"{current_path},{last_job}")

    return free_slots

def main(test=False):
    """ Main function. """
    if test:
        print("\nThis is a test.")
    exe = get_config("exe")
    last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
    constraints = get_config("constraints")
    for constraint in constraints:
        free_slots = st.get_free_slots(constraint)
        print(f"\n{color.BOLD}{constraint}:{color.RESET} {color.CYAN}{free_slots}{color.RESET} free slots.")
        if test and not free_slots:
            free_slots = 100
        while free_slots:
            free_slots = process_variant(constraint, free_slots, test, last_job_file)
    print()

if __name__ == "__main__":
    DESCRIPTION = "Submit jobs."
    FLAG = "--test"
    FLAG_HELP = "Run test"
    args = parse_args(DESCRIPTION, FLAG, FLAG_HELP)
    main(test=args.test)
