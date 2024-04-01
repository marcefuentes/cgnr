#!/usr/bin/env python

import argparse
import logging
import os
import sys

import modules.slurm_tools as st
import tools.colors as cc
from tools.list_of_folders import list_of_folders
from tools.get_config import get_config

# Purpose: browse through folders and submit jobs
# Usage: python submit.py or python submit.py test

def get_job_min(current_path):
    input_file_extension = get_config("input_file_extension")
    job_min = 9999
    for file in os.listdir(current_path):
        if file.endswith(input_file_extension):
            basename = int(file.split(".")[0])
            if basename < job_min:
                job_min = basename
    return job_min

def get_job_max(current_path):
    input_file_extension = get_config("input_file_extension")
    job_max = 0
    for file in os.listdir(current_path):
        if file.endswith(input_file_extension):
            basename = int(file.split(".")[0])
            if basename > job_max:
                job_max = basename
    return job_max

def process_folder(constraint, free_slots, last_job, test):
    output_file_extension, *_ = get_config("output_file_extensions")
    current_path = os.getcwd()
    current_path_folders = current_path.split("/")
    current_path_print = "/".join(current_path_folders[-3:])
    if last_job == 0:
        job_min = get_job_min(current_path)
    else:
        job_min = last_job + 1
    if os.path.isfile(os.path.join(current_path, f"{job_min}{output_file_extension}")):
        print(f"{cc.red}{current_path_print}/{job_min}{output_file_extension} already exists.{cc.reset}")
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
        return_code, stdout, stderr = st.submit_job(current_path_folders, job_array_string, constraint)
    if return_code != 0:
        print(f"{cc.red}sbatch command failed with return code {return_code}.{cc.reset}")
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
    print(f"{cc.green}{info}.{cc.reset}")
    free_slots -= num_jobs_to_submit
    if last_job == job_max:
        last_job = 0
    return free_slots, last_job

def process_variant(constraint, free_slots, test, last_job_file):
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r") as f:
            current_path, last_job = f.read().strip().split(",")
        last_job = int(last_job)
    else:
        if test:
            print("Submission is about to start in a new variant. Cannot run with --test option.")
            exit()
        mechanisms = list_of_folders(os.getcwd())
        givens = list_of_folders(mechanisms[0])
        current_path = givens[0]
        current_path_folders = current_path.split("/")
        current_path_print = "/".join(current_path_folders[-3:])
        print(f"\n{cc.bold}Submit jobs in {current_path_print}?{cc.reset} {cc.yesno} ", end="")
        user_input = input()
        if user_input.lower() == "n":
            exit()
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
                    print(f"Would remove {last_job_file}.{cc.reset}")
                else:
                    os.remove(last_job_file)
                print(f"{cc.bold}{cc.green}All jobs submitted.{cc.reset}")
                print(f"{cc.bold}{cc.cyan}{free_slots}{cc.reset} free slots in {cc.bold}{constraint}{cc.reset}.\n")
                exit()
    if test:
        print(f"Would write {current_path},{last_job} to {last_job_file}.{cc.reset}")
    else:
        with open(last_job_file, "w") as f:
            f.write(f"{current_path},{last_job}")

    return free_slots

def main(test=False):

    if test:
        print(f"\nThis is a test.")
    exe = get_config("exe")
    last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
    log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.log"
    logging.basicConfig(filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s")
    constraints = get_config("constraints")
    for constraint in constraints:
        free_slots = st.get_free_slots(constraint)
        print(f"\n{cc.bold}{constraint}:{cc.reset} {cc.cyan}{free_slots}{cc.reset} free slots.")
        if test and not free_slots:
            free_slots = 100
        while free_slots:
            free_slots = process_variant(constraint, free_slots, test, last_job_file)
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit jobs")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()

    main(test=args.test)
