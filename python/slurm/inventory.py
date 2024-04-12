#!/usr/bin/env python

""" Show status of simulations."""

import csv
import os
import sys

import common_modules.color as color
from common_modules.get_config import get_config
from modules.argparse_utils import parse_args
from modules.slurm_tools import get_squeue_stats, slots
from modules.list_of_folders import list_of_folders
import submit

def get_results_path(store=False):
    """Get the path to the results folder."""
    exe = get_config("exe")
    if store:
        store_path = os.environ.get("STORE")
        if store_path is None:
            raise ValueError("STORE environment variable not set")
        return f"{store_path}/code/{exe}/results"
    home_path = os.environ.get("HOME")
    return f"{home_path}/code/{exe}/results"

def process_variant(current_path):
    """Process a variant folder."""

    folder_dict = {}

    variant = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{color.CYAN}{variant}{color.RESET}")
    else:
        print(f"\n{color.WHITE}{variant}{color.RESET}")

    if "noshuffle" in variant:
        folder_dict["Shuffle"] = 0
    else:
        folder_dict["Shuffle"] = 1
    if "_d" in variant:
        folder_dict["DeathRate"] = -3
    else:
        folder_dict["DeathRate"] = -7
    if "nolang" in variant:
        folder_dict["Language"] = 0
    else:
        folder_dict["Language"] = 0
    cost_index = variant.find("cost")
    cost = variant[cost_index + 4:cost_index + 6]
    folder_dict["Cost"] = -int(cost)
    if "_128" in variant:
        folder_dict["GroupSize"] = 7
    elif "_16" in variant:
        folder_dict["GroupSize"] = 4
    elif "_8" in variant:
        folder_dict["GroupSize"] = 3
    else:
        folder_dict["GroupSize"] = 2

    mechanisms = list_of_folders(current_path)
    for mechanism in mechanisms:
        process_mechanism(mechanism, folder_dict)

def process_mechanism(current_path, folder_dict):
    """Process a mechanism folder."""

    mechanism = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{color.CYAN}{mechanism}{color.RESET}", end = "")
    else:
        print(f"{color.WHITE}{mechanism}{color.RESET}", end = "")

    if "p" in mechanism:
        folder_dict["PartnerChoice"] = 1
    else:
        folder_dict["PartnerChoice"] = 0
    if "i" in mechanism:
        folder_dict["Reciprocity"] = 1
        folder_dict["IndirectR"] = 1
    elif "r" in mechanism:
        folder_dict["Reciprocity"] = 1
        folder_dict["IndirectR"] = 0
    else:
        folder_dict["Reciprocity"] = 0
        folder_dict["IndirectR"] = 0

    givens = list_of_folders(current_path)
    for given in givens:
        process_given(given, folder_dict)

def process_given(current_path, folder_dict):
    """Process a given folder."""

    number_of_lines = get_config("number_of_lines")
    input_file_extension = get_config("input_file_extension")
    output_file_extension, *_ = get_config("output_file_extensions")

    current_path_folders = current_path.split("/")
    given = current_path_folders[-1]
    if os.path.islink(current_path):
        print(f"{color.CYAN}\t{given}{color.RESET}", end = "  ")
    else:
        print(f"{color.WHITE}\t{given}{color.RESET}", end = "  ")

    folder_dict["Given"] = float(given[-3:]) / 100

    input_files = [f for f in os.listdir(current_path) if f.endswith(input_file_extension)]
    total_jobs = len(input_files)
    if total_jobs == 0:
        print(f"{color.BOLD}{color.RED}no {input_file_extension[1:]} files{color.RESET}")
        return
    with open(os.path.join(current_path, input_files[0]), "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = row
            if key == "Given":
                if float(value) != folder_dict[key]:
                    print(f"{color.BOLD}{color.RED}{key} {folder_dict[key]} {value}{color.RESET}", end = " ")
            elif key in folder_dict:
                if int(value) != folder_dict[key]:
                    print(f"{color.BOLD}{color.RED}{key} {folder_dict[key]} {value}{color.RESET}", end = " ")

    finished_jobs = 0
    garbled_jobs = 0
    no_header = 0
    one_line_jobs = 0

    output_files = [f for f in os.listdir(current_path) if f.endswith(output_file_extension)]
    for output_file in output_files:
        with open(os.path.join(current_path, output_file), "r", encoding="utf-8") as f:
            n_lines = sum(1 for line in f)
            if n_lines == number_of_lines:
                finished_jobs += 1
            elif n_lines == 1:
                one_line_jobs += 1
            elif n_lines == number_of_lines - 1:
                no_header += 1
            else:
                garbled_jobs += 1
    mechanism = current_path_folders[-2]
    variant = current_path_folders[-3]
    jobname =  f"{mechanism}_{given}_{variant}"
    if "mfu" in current_path and "Store" not in current_path:
        running_jobs = get_squeue_stats("name", jobname, "running")
        pending_jobs = get_squeue_stats("name", jobname, "pending")
        dead_jobs = one_line_jobs - running_jobs
    else:
        running_jobs = 0
        pending_jobs = one_line_jobs
        dead_jobs = 0
    to_submit_jobs = (
        total_jobs
        - pending_jobs
        - running_jobs
        - finished_jobs
        - garbled_jobs
        - no_header
        - dead_jobs
    )

    print(f"{color.BOLD}{color.GREEN}{finished_jobs:>4}{color.RESET}" if finished_jobs else   "", end = "")
    print(f"{color.BOLD}{color.YELLOW}{running_jobs:>4}{color.RESET}" if running_jobs else    "", end = "")
    print(f"{color.BOLD}{color.WHITE}{pending_jobs:>4}{color.RESET}"  if pending_jobs else    "", end = "")
    print(f"{color.BOLD}{color.GREY}{to_submit_jobs:>4}{color.RESET}" if to_submit_jobs else  "", end = "")
    print(f"{color.BOLD}{color.RED}{dead_jobs:>4}{color.RESET}"       if dead_jobs else       "", end = "")
    print(f"{color.BOLD}{color.purple}{no_header:>4}{color.RESET}"    if no_header else       "", end = "")
    print(f"{color.BOLD}{color.BLUE}{garbled_jobs:>4}{color.RESET}"   if garbled_jobs else    "", end = "")
    print()

def main(store=False):
    """Main function."""

    current_path = get_results_path(store)

    if os.path.isdir(current_path):
        os.chdir(current_path)
    else:
        print(f"{color.BOLD}{color.RED}Directory {current_path} does not exist{color.RESET}")
        sys.exit()

    print(f"\n{color.WHITE}{current_path}{color.RESET}")
    for variant in list_of_folders(current_path):
        process_variant(variant)
    if "mfu" in current_path and not store:
        # Print - 30 times
        print(f"\n{color.WHITE}{'-' * 30}{color.RESET}")
        free_slots = slots()
        if free_slots:
            exe = get_config("exe")
            last_job_file = f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
            if os.path.isfile(last_job_file):
                msg = (
                    f"\n{color.BOLD}Submit {color.CYAN}{free_slots}{color.RESET}{color.BOLD} jobs{color.RESET} "
                    f"{color.YESNO} "
                )
                print(msg, end="")
                user_input = input()
                if user_input.lower() == "n":
                    print()
                    sys.exit()
                submit.main()
            else:
                msg = (
                    "\nTo submit jobs, go to a variant folder with "
                    "no running or finished jobs and run submit\n"
                )
                print(msg)
        else:
            print()
    else:
        print()

if __name__ == "__main__":
    DESCRIPTION = "Show status of simulations."
    FLAG = "--store"
    FLAG_HELP = "inventory 'Store' filesystem in cesga"
    args = parse_args(DESCRIPTION, FLAG, FLAG_HELP)
    main(store=args.store)
