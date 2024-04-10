#!/usr/bin/env python

""" Resubmit unfinished jobs """

import os
import sys

import common_modules.colors as cc
from common_modules.get_config import get_config
from modules.argparse_utils import parse_args
from modules.process_jobs import process_jobs
import modules.slurm_tools as st

# Purpose: resubmit unfinished jobs
# Usage: python resubmit.py

def process_folder(test):
    """ Prepare jobs in the current folder """

    exe = get_config("exe")
    last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"

    current_path = os.getcwd()
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r", encoding="utf-8") as f:
            last_job_file_path, _ = f.read().strip().split(",")
        if last_job_file_path == current_path:
            print(f"{cc.red}{last_job_file.split('/')[-1]} points to this folder.{cc.reset}")
            print(f"{cc.red}Run submit first.{cc.reset}")
            if test:
                print("If this were not a test, the program would stop here.\n")
            else:
                sys.exit()
    current_path_folders = current_path.split("/")
    jobs_to_submit = st.get_jobs_to_submit(current_path_folders)
    if len(jobs_to_submit) == 0:
        print(f"\n{cc.green}No jobs to submit.\n{cc.reset}")
        sys.exit()
    print(f"\n{cc.cyan}{len(jobs_to_submit)}{cc.reset} jobs to submit.\n")

    if test:
        msg = (
            f"{cc.white}Would delete output files of jobs in {cc.reset}"
            f"{cc.red}red{cc.white} and {cc.grey}grey{cc.reset}."
        )
        print(msg)
    else:
        print(f"{cc.bold}{cc.red}This is not a test!{cc.reset}")
        msg = (
            f"{cc.white}Delete output files of jobs in {cc.reset}"
            f"{cc.red}red{cc.white} and {cc.grey}grey {cc.reset}"
            f"{cc.yesno} "
        )
        print(msg, end="")
        user_input = input()
        if user_input.lower() == "n":
            sys.exit()
        st.remove_files(jobs_to_submit)

    constraints = get_config("constraints")
    for constraint in constraints:
        if len(jobs_to_submit) == 0:
            print(f"{cc.green}No jobs to submit.\n{cc.reset}")
            sys.exit()
        free_slots = st.get_free_slots(constraint)
        print(f"\n{constraint}:{cc.reset} {cc.cyan}{free_slots}{cc.reset} free slots.")
        if not free_slots:
            print(f"{cc.red}{len(jobs_to_submit)}{cc.reset} jobs remain to be submitted.")
            continue
        num_jobs_to_submit = min(free_slots, len(jobs_to_submit))
        job_array_string = ",".join(map(str, jobs_to_submit[:num_jobs_to_submit]))
        process_jobs(current_path_folders, job_array_string, constraint, test)
        del jobs_to_submit[:num_jobs_to_submit]
        free_slots -= num_jobs_to_submit
        print(f"{cc.cyan}{free_slots}{cc.reset} free slots in {constraint}.{cc.reset}")
        if not free_slots:
            print(f"{cc.red}{len(jobs_to_submit)}{cc.reset} jobs remain to be submitted.")

def main(test):
    """ Main function """
    process_folder(test)

if __name__ == "__main__":
    DESCRIPTION = "Resubmit unfinished jobs."
    FLAG = "--test"
    FLAG_HELP = "Run test"
    args = parse_args(DESCRIPTION, FLAG, FLAG_HELP)
    main(test=args.test)
