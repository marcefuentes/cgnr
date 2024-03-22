#!/usr/bin/env python

import logging
import os
import sys

import slurm.tools as st
import tools.colors as cc
from slurm.get_config import get_config
from slurm.tools import get_free_slots

# Purpose: resubmit unfinished jobs
# Usage: python resubmit.py

queues = ["clk", "epyc"]

def submit_jobs_in_folder(current_path, jobs_to_submit, test=False):
    for queue in queues:
        if len(jobs_to_submit) == 0:
            print(f"{cc.bold}{cc.green}No jobs to submit\n{cc.reset_format}")
            exit()
        free_slots = get_free_slots(queue)
        print(f"\n{cc.bold}{queue}:{cc.reset_format} {cc.cyan}{free_slots}{cc.reset_format} free slots")
        if not free_slots:
            continue
        num_jobs_to_submit = min(free_slots, len(jobs_to_submit))
        job_array = ",".join(map(str, jobs_to_submit[:num_jobs_to_submit]))
        last_job = jobs_to_submit[num_jobs_to_submit - 1]
        current_path_folders = current_path.split("/")
        variant = current_path_folders[-3]
        mechanism = current_path_folders[-2]
        if test:
            return_code = 0
            stdout = "test"
            stderr = "test"
        else:
            return_code, stdout, stderr = st.submit_job(variant, mechanism, last_job, queue, job_array)
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
        current_path_print = "/".join(current_path_folders[-3:])
        info = f"{current_path_print}/{job_array} to {queue}"
        logging.info(info)
        print(f"{cc.green}{info}{cc.reset_format}")
        del jobs_to_submit[:num_jobs_to_submit]
        free_slots -= num_jobs_to_submit
        print(f"{cc.bold}{cc.cyan}{free_slots}{cc.reset_format} free slots in {cc.bold}{queue}{cc.reset_format}\n")
    print(f"{cc.bold}{cc.red}{len(jobs_to_submit)}{cc.reset_format} jobs remain to be submitted")

def main():

    try:
        exe = get_config("exe")
    except RuntimeError as e:
        print(f"{cc.red}{e}{cc.reset_format}")
        exit()

    test = len(sys.argv) > 1
    if test:
        print(f"\n{cc.bold}This is a test\n{cc.reset_format}")
        log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.test"
    else:
        print(f"\n{cc.bold}{cc.red}This is not a test! {cc.white}Continue?{cc.reset_format} {cc.yesno} ", end="")
        user_input = input()
        if user_input.lower() == "n":
            exit()
        log_file = f"/home/ulc/ba/mfu/code/{exe}/results/submit.log"
    last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
    logging.basicConfig(filename=log_file,
                        level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s")

    current_path = os.getcwd()
    if os.path.isfile(last_job_file):
        with open(last_job_file, "r") as f:
            last_job_file_path, last_job = f.read().strip().split(",")
        if last_job_file_path == current_path:
            print(f"\n{cc.bold}{cc.red}{last_job_file.split('/')[-1]} points to this folder. Run submit.py first.{cc.reset_format}")
            if test:
                print(f"If this were not a test, the program would end here\n")
            else:
                exit()
    jobs_to_submit = st.get_jobs_to_submit(current_path)
    if len(jobs_to_submit) == 0:
        print(f"\n{cc.bold}{cc.green}No jobs to submit\n{cc.reset_format}")
        return
    print(f"\n{cc.bold}{cc.cyan}{len(jobs_to_submit)}{cc.reset_format} jobs to submit.")

    if test:
        print(f"\n{cc.bold}{cc.red}Would delete current output files of {jobs_to_submit}{cc.reset_format}")
    else:
        print(f"\n{cc.bold}{cc.red}This is not a test! {cc.white}Delete output files of {jobs_to_submit} and resubmit?{cc.reset_format} {cc.yesno} ", end="")
        user_input = input()
        if user_input.lower() == "n":
            exit()
        st.remove_files(jobs_to_submit)

    submit_jobs_in_folder(current_path, jobs_to_submit, test)

    print()

if __name__ == "__main__":
    main()
