#!/usr/bin/env python

""" Submit jobs. """

import os
import sys

from modules.parse_args import parse_args
from modules.list_of_folders import list_of_folders
from modules.process_jobs import process_jobs
import modules.slurm_tools as st
from python_colors.colors import ask, colors
from settings_project.project import project

# Purpose: browse through folders and submit jobs
# Usage: python submit.py or python submit.py test


def get_job_max(work_path):
    """Get the maximum job number in the work folder."""

    input_file_extension = project["input_file_extension"]
    job_max = 0
    for file in os.listdir(work_path):
        if file.endswith(input_file_extension):
            basename = int(file.split(".")[0])
            job_max = max(job_max, basename)
    return job_max


def get_job_min(work_path):
    """Get the minimum job number in the work folder."""

    input_file_extension = project["input_file_extension"]
    job_min = 9999
    for file in os.listdir(work_path):
        if file.endswith(input_file_extension):
            basename = int(file.split(".")[0])
            job_min = min(job_min, basename)
    return job_min


def next_work_path(work_path):
    """Get the next work path."""

    mechanism = os.path.dirname(work_path)
    givens = list_of_folders(mechanism)
    given_index = givens.index(work_path) + 1
    if given_index < len(givens):
        return False, givens[given_index]
    mechanisms = list_of_folders(os.path.dirname(mechanism))
    mechanism_index = mechanisms.index(mechanism) + 1
    if mechanism_index < len(mechanisms):
        mechanism = mechanisms[mechanism_index]
        givens = list_of_folders(mechanism)
        return False, givens[0]
    return True, work_path


def process_folder(constraint, free_slots, last_job, test):
    """Submit jobs in the work folder"""

    output_file_extension, *_ = project["output_file_extensions"]
    work_path = os.getcwd()
    work_path_folders = work_path.split("/")
    work_path_print = "/".join(work_path_folders[-3:])
    if last_job == 0:
        job_min = get_job_min(work_path)
    else:
        job_min = last_job + 1
    if os.path.isfile(os.path.join(work_path, f"{job_min}{output_file_extension}")):
        print(
            f"{colors['red']}{work_path_print}/{job_min}{output_file_extension} "
            f"already exists.{colors['reset']}"
        )
        last_job = 0
        return free_slots, last_job
    job_max = get_job_max(work_path)
    num_jobs_to_submit = min(free_slots, job_max - job_min + 1)
    last_job = job_min + num_jobs_to_submit - 1
    job_array_string = f"{job_min}-{last_job}"
    process_jobs(work_path_folders, job_array_string, constraint, test)
    free_slots -= num_jobs_to_submit
    if last_job == job_max:
        last_job = 0
    return free_slots, last_job


def process_variant(constraint, free_slots, test, last_job_file):
    """Process the parent directory."""

    if os.path.isfile(last_job_file):
        with open(last_job_file, "r", encoding="utf-8") as f:
            work_path, last_job = f.read().strip().split(",")
        last_job = int(last_job)
    else:
        if test:
            print(
                "Submission is about to start in a new variant. Cannot run with --test option."
            )
            sys.exit()
        mechanisms = list_of_folders(os.getcwd())
        givens = list_of_folders(mechanisms[0])
        work_path = givens[0]
        work_path_folders = work_path.split("/")
        work_path_print = "/".join(work_path_folders[-3:])
        print(
            f"\n{colors['bold']}Submit jobs in {work_path_print}?{colors['reset']} "
            f"{ask['yesno']}", end=""
        )
        user_input = input()
        if user_input.lower() == "n":
            sys.exit()
        last_job = 0
    os.chdir(work_path)
    free_slots, last_job = process_folder(constraint, free_slots, last_job, test)

    if last_job == 0:
        all_submitted, work_path = next_work_path(work_path)
        if all_submitted:
            if test:
                print(f"Would remove {last_job_file}.{colors['reset']}")
            else:
                os.remove(last_job_file)
            print(
                f"{colors['bold']}{colors['green']}All jobs submitted{colors['reset']}\n"
                + f"{colors['bold']}{colors['cyan']}{free_slots}{colors['reset']} "
                + f"free slots in {colors['bold']}{constraint}{colors['reset']}\n"
            )
            sys.exit()
    if test:
        print(
            f"Would write {work_path},{last_job} to {last_job_file}.{colors['reset']}"
        )
    else:
        with open(last_job_file, "w", encoding="utf-8") as f:
            f.write(f"{work_path},{last_job}")

    return free_slots


def main(test=False):
    """Main function."""

    if test:
        print("\nThis is a test.")
    exe = os.environ["PROJECT"]
    last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
    constraints = project["constraints"]
    for constraint in constraints:
        free_slots = st.get_free_slots(constraint)
        print(
            f"\n{colors['bold']}{constraint}:{colors['reset']}"
            + f"{colors['cyan']}{free_slots}{colors['reset']} free slots"
        )
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
