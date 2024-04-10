#!/usr/bin/env python

""" Submit jobs. """

import logging
import os
import sys

import common_modules.colors as cc
from common_modules.get_config import get_config
import modules.slurm_tools as st
from modules.list_of_folders import list_of_folders
from modules.argparse_utils import parse_args

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
            f"{cc.RED}{current_path_print}/{job_min}{output_file_extension} "
            f"already exists.{cc.RESET}"
        )
        print(msg)
        last_job = 0
        return free_slots, last_job
    job_max = get_job_max(current_path)
    num_jobs_to_submit = min(free_slots, job_max - job_min + 1)
    last_job = job_min + num_jobs_to_submit - 1
    job_array_string = f"{job_min}-{last_job}"
    info = f"{current_path_print}/{job_array_string} to {constraint}"
    if test:
        print(f"Would submit {info}.")
        return_code = 0
        stdout = "Test"
        stderr = "Test"
    else:
        return_code, stdout, stderr = st.submit_job(
            current_path_folders,
            job_array_string,
            constraint
        )
    if return_code != 0:
        print(f"{cc.RED}sbatch command failed with return code {return_code}.{cc.RESET}")
        if stderr:
            print(stderr)
            logging.error(stderr)
        sys.exit()
    else:
        for line in stdout.split("\n"):
            if line:
                print(line)
                logging.info(line)
    logging.info(info)
    print(f"{cc.GREEN}{info}.{cc.RESET}")
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
        print(f"\n{cc.BOLD}Submit jobs in {current_path_print}?{cc.RESET} {cc.YESNO} ", end="")
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
                    print(f"Would remove {last_job_file}.{cc.RESET}")
                else:
                    os.remove(last_job_file)
                print(f"{cc.BOLD}{cc.GREEN}All jobs submitted.{cc.RESET}")
                msg = (
                    f"{cc.BOLD}{cc.CYAN}{free_slots}{cc.RESET} "
                    f"free slots in {cc.BOLD}{constraint}{cc.RESET}.\n"
                )
                print(msg)
                sys.exit()
    if test:
        print(f"Would write {current_path},{last_job} to {last_job_file}.{cc.RESET}")
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
    log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    constraints = get_config("constraints")
    for constraint in constraints:
        free_slots = st.get_free_slots(constraint)
        print(f"\n{cc.BOLD}{constraint}:{cc.RESET} {cc.CYAN}{free_slots}{cc.RESET} free slots.")
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
