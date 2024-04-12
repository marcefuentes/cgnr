#!/usr/bin/env python

""" Resubmit unfinished jobs """

import logging
import os
import sys

import common_modules.color as color
from common_modules.get_config import get_config
from modules.argparse_utils import parse_args
import modules.slurm_tools as st

# Purpose: resubmit unfinished jobs
# Usage: python resubmit.py

def submit_jobs_in_folder(current_path_folders, jobs_to_submit, test):
    """ Submit jobs in the current folder """

    current_path_print = "/".join(current_path_folders[-3:])
    constraints = get_config("constraints")
    for constraint in constraints:
        if len(jobs_to_submit) == 0:
            print(f"{color.GREEN}No jobs to submit.\n{color.RESET}")
            sys.exit()
        free_slots = st.get_free_slots(constraint)
        print(f"\n{constraint}:{color.RESET} {color.CYAN}{free_slots}{color.RESET} free slots.")
        if not free_slots:
            print(f"{color.RED}{len(jobs_to_submit)}{color.RESET} jobs remain to be submitted.")
            continue
        num_jobs_to_submit = min(free_slots, len(jobs_to_submit))
        job_array_string = ",".join(map(str, jobs_to_submit[:num_jobs_to_submit]))
        info = f"{current_path_print}/{job_array_string} to {constraint}"
        if test:
            print(f"Would submit {info}.")
            return_code = 0
            stderr = "Test"
            stdout = "Test"
        else:
            return_code, stdout, stderr = st.submit_job(
                current_path_folders,
                job_array_string,
                constraint
            )
        if return_code != 0:
            print(f"{color.RED}sbatch command failed with return code {return_code}.{color.RESET}")
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
        print(f"{color.GREEN}{info}.{color.RESET}")
        del jobs_to_submit[:num_jobs_to_submit]
        free_slots -= num_jobs_to_submit
        print(f"{color.CYAN}{free_slots}{color.RESET} free slots in {constraint}.{color.RESET}")
        if not free_slots:
            print(f"{color.RED}{len(jobs_to_submit)}{color.RESET} jobs remain to be submitted.")

def main(test=False):
    """ Main function """

    exe = get_config("exe")
    if test:
        print("\nThis is a test.\n")
        log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.test"
    else:
        msg = (
            f"\n{color.BOLD}{color.RED}This is not a test! {color.WHITE}Continue?{color.RESET} "
            f"{color.YESNO} "
        )
        print(msg, end="")
        user_input = input()
        if user_input.lower() == "n":
            sys.exit()
        log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.log"
    last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    current_path = os.getcwd()
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r", encoding="utf-8") as f:
            last_job_file_path, _ = f.read().strip().split(",")
        if last_job_file_path == current_path:
            print(f"{color.RED}{last_job_file.split('/')[-1]} points to this folder.{color.RESET}")
            print(f"{color.RED}Run submit first.{color.RESET}")
            if test:
                print("If this were not a test, the program would end here.\n")
            else:
                sys.exit()
    current_path_folders = current_path.split("/")
    jobs_to_submit = st.get_jobs_to_submit(current_path_folders)
    if len(jobs_to_submit) == 0:
        print(f"\n{color.GREEN}No jobs to submit.\n{color.RESET}")
        return
    print(f"\n{color.CYAN}{len(jobs_to_submit)}{color.RESET} jobs to submit.\n")

    if test:
        msg = (
            f"{color.WHITE}Would delete output files of jobs in {color.RESET}"
            f"{color.RED}red{color.WHITE} and {color.GREY}grey{color.RESET}."
        )
        print(msg)
    else:
        print(f"{color.BOLD}{color.RED}This is not a test!{color.RESET}")
        msg = (
            f"{color.WHITE}Delete output files of jobs in {color.RESET}"
            f"{color.RED}red{color.WHITE} and {color.GREY}grey {color.RESET}"
            f"{color.YESNO} "
        )
        print(msg, end="")
        user_input = input()
        if user_input.lower() == "n":
            sys.exit()
        st.remove_files(jobs_to_submit)

    submit_jobs_in_folder(current_path_folders, jobs_to_submit, test)

    print()

if __name__ == "__main__":
    DESCRIPTION = "Resubmit unfinished jobs."
    FLAG = "--test"
    FLAG_HELP = "Run test"
    args = parse_args(DESCRIPTION, FLAG, FLAG_HELP)
    main(test=args.test)
