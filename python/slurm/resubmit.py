#!/usr/bin/env python

""" Resubmit unfinished jobs """

import os
import sys

from modules.argparse_utils import parse_args
from modules.process_jobs import process_jobs
import modules.slurm_tools as st
from python_colors.colors import ask, colors
from settings_project.project import project

# Purpose: resubmit unfinished jobs
# Usage: python resubmit.py


def process_folder(test):
    """Prepare jobs in the current folder"""

    exe = os.environ["PROJECT"]
    last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"

    current_path = os.getcwd()
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r", encoding="utf-8") as f:
            last_job_file_path, _ = f.read().strip().split(",")
        if last_job_file_path == current_path:
            print(
                f"{colors['red']}{last_job_file.split('/')[-1]} points to this folder."
                f"{colors['reset']}"
            )
            print(f"{colors['red']}Run submit first.{colors['reset']}")
            if test:
                print("If this were not a test, the program would stop here.\n")
            else:
                sys.exit()
    current_path_folders = current_path.split("/")
    jobs_to_submit = st.get_jobs_to_submit(current_path_folders)
    if len(jobs_to_submit) == 0:
        print(f"\n{colors['green']}No jobs to submit.\n{colors['reset']}")
        sys.exit()
    print(f"\n{colors['cyan']}{len(jobs_to_submit)}{colors['reset']} jobs to submit.\n")

    if test:
        print(
            f"{colors['white']}Would delete output files of jobs in {colors['reset']}"
            f"{colors['red']}red{colors['white']} and {colors['grey']}grey{colors['reset']}."
        )
    else:
        print(f"{colors['bold']}{colors['red']}This is not a test!{colors['reset']}")
        print(
            f"{colors['white']}Delete output files of jobs in {colors['reset']}"
            f"{colors['red']}red{colors['white']} and {colors['grey']}grey{colors['reset'] }"
            f"{ask['yesno']}"
        )
        user_input = input()
        if user_input.lower() == "n":
            sys.exit()
        st.remove_files(jobs_to_submit)

    constraints = project["constraints"]
    for constraint in constraints:
        if len(jobs_to_submit) == 0:
            print(f"{colors['green']}No jobs to submit.\n{colors['reset']}")
            sys.exit()
        free_slots = st.get_free_slots(constraint)
        print(
            f"\n{constraint}: {colors['cyan']}{free_slots}{colors['reset']} free slots"
        )
        if not free_slots:
            print(
                f"{colors['red']}{len(jobs_to_submit)}{colors['reset']} jobs remain to be submitted"
            )
            continue
        num_jobs_to_submit = min(free_slots, len(jobs_to_submit))
        job_array_string = ",".join(map(str, jobs_to_submit[:num_jobs_to_submit]))
        process_jobs(current_path_folders, job_array_string, constraint, test)
        del jobs_to_submit[:num_jobs_to_submit]
        free_slots -= num_jobs_to_submit
        print(
            f"{colors['cyan']}{free_slots}{colors['reset']} free slots in {constraint}."
        )
        if not free_slots:
            print(
                f"{colors['red']}{len(jobs_to_submit)}{colors['reset']}"
                f" jobs remain to be submitted."
            )


def main(test):
    """Main function"""

    process_folder(test)


if __name__ == "__main__":
    DESCRIPTION = "Resubmit unfinished jobs."
    FLAG = "--test"
    FLAG_HELP = "Run test"
    args = parse_args(DESCRIPTION, FLAG, FLAG_HELP)
    main(test=args.test)
