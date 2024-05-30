#!/usr/bin/env python

""" Shows status of simulations."""

import csv
import os
import sys

from modules.argparse_utils import parse_args
from modules.slurm_tools import get_squeue_stats, slots
from modules.list_of_folders import list_of_folders
from python_colors.colors import colors
from settings_project.project import project
import submit


def find_errors(current_path, input_file, folder_data):
    """Process a given folder for errors in input files."""

    given_value = float(current_path.split("/")[-1])
    folder_data["Given"] = given_value

    with open(os.path.join(current_path, input_file), "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for key, value in reader:
            expected_value = folder_data.get(key)
            if expected_value is not None and expected_value != float(value):
                print(
                    f"{colors['bold']}{colors['red']}{key} {expected_value} {value}{colors['reset']}",
                    end=" ",
                )


def get_results_path(store=False):
    """Get the path to the results folder."""

    exe = os.environ["PROJECT"]
    if store:
        store_path = os.environ.get("STORE")
        if store_path is None:
            raise ValueError("STORE environment variable not set")
        return f"{store_path}/code/{exe}/results"
    home_path = os.environ.get("HOME")
    return f"{home_path}/code/{exe}/results"


def job_status(current_path, total_jobs):
    """Find status of jobs in a given folder."""

    output_file_extension, *_ = project["output_file_extensions"]
    finished_jobs = 0
    garbled_jobs = 0
    no_header = 0
    one_line_jobs = 0

    for output_file in [
        f for f in os.listdir(current_path) if f.endswith(output_file_extension)
    ]:
        with open(os.path.join(current_path, output_file), "r", encoding="utf-8") as f:
            n_lines = sum(1 for line in f)
            if n_lines == project["number_of_lines"]:
                finished_jobs += 1
            elif n_lines == 1:
                one_line_jobs += 1
            elif n_lines == project["number_of_lines"] - 1:
                no_header += 1
            else:
                garbled_jobs += 1

    job_name = f"{current_path.split('/')[-2]}"
    job_name += f"_{current_path.split('/')[-1]}"
    job_name += f"_{current_path.split('/')[-3]}"
    if "mfu" in current_path and "Store" not in current_path:
        running_jobs = get_squeue_stats("name", job_name, "running")
        pending_jobs = get_squeue_stats("name", job_name, "pending")
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

    print(
        (
            f"{colors['bold']}{colors['green']}{finished_jobs:>4}{colors['reset']}"
            if finished_jobs
            else ""
        ),
        end="",
    )
    print(
        (
            f"{colors['bold']}{colors['yellow']}{running_jobs:>4}{colors['reset']}"
            if running_jobs
            else ""
        ),
        end="",
    )
    print(
        (
            f"{colors['bold']}{colors['white']}{pending_jobs:>4}{colors['reset']}"
            if pending_jobs
            else ""
        ),
        end="",
    )
    print(
        (
            f"{colors['bold']}{colors['grey']}{to_submit_jobs:>4}{colors['reset']}"
            if to_submit_jobs
            else ""
        ),
        end="",
    )
    print(
        (
            f"{colors['bold']}{colors['red']}{dead_jobs:>4}{colors['reset']}"
            if dead_jobs
            else ""
        ),
        end="",
    )
    print(
        (
            f"{colors['bold']}{colors['purple']}{no_header:>4}{colors['reset']}"
            if no_header
            else ""
        ),
        end="",
    )
    print(
        (
            f"{colors['bold']}{colors['blue']}{garbled_jobs:>4}{colors['reset']}"
            if garbled_jobs
            else ""
        ),
        end="",
    )
    print()


def process_given(current_path, folder_data):
    """Process a given folder."""

    current_path_folders = current_path.split("/")
    given = current_path_folders[-1]

    if os.path.islink(current_path):
        print(f"{colors['cyan']}\t{given:<5}{colors['reset']}", end="")
    else:
        print(f"{colors['white']}\t{given:<5}{colors['reset']}", end="")

    input_file_extension = project["input_file_extension"]
    input_files = [
        f for f in os.listdir(current_path) if f.endswith(input_file_extension)
    ]

    find_errors(current_path, input_files[0], folder_data)

    total_jobs = len(input_files)
    if total_jobs == 0:
        print(
            f"{colors['bold']}{colors['red']}no {input_file_extension[1:]} files{colors['reset']}"
        )
        return

    job_status(current_path, total_jobs)


def process_mechanism(current_path, folder_data):
    """Process a mechanism folder."""

    mechanism = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{colors['cyan']}{mechanism}{colors['reset']}", end="")
    else:
        print(f"{colors['white']}{mechanism}{colors['reset']}", end="")

    if "p" in mechanism:
        folder_data["PartnerChoice"] = 1
    else:
        folder_data["PartnerChoice"] = 0
    if "i" in mechanism:
        folder_data["Reciprocity"] = 1
        folder_data["IndirectR"] = 1
    elif "d" in mechanism:
        folder_data["Reciprocity"] = 1
        folder_data["IndirectR"] = 0
    else:
        folder_data["Reciprocity"] = 0
        folder_data["IndirectR"] = 0

    givens = list_of_folders(current_path)
    for given in givens:
        process_given(given, folder_data)


def process_variant(current_path):
    """Process a variant folder."""

    folder_data = {}

    variant = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{colors['cyan']}{variant}{colors['reset']}")
    else:
        print(f"\n{colors['white']}{variant}{colors['reset']}")

    folder_data["Shuffle"] = "noshuffle" not in variant
    folder_data["Language"] = "nolang" not in variant
    cost_index = variant.find("cost")
    cost = variant[cost_index + 4 : cost_index + 6]
    folder_data["Cost"] = -int(cost)
    if "_128" in variant:
        folder_data["GroupSize"] = 7
    else:
        folder_data["GroupSize"] = 2

    mechanisms = list_of_folders(current_path)
    for mechanism in mechanisms:
        process_mechanism(mechanism, folder_data)


def main(store=False):
    """Main function."""

    current_path = get_results_path(store)

    if os.path.isdir(current_path):
        os.chdir(current_path)
    else:
        print(
            f"{colors['bold']}{colors['red']}Directory {current_path} does not exist{colors['reset']}"
        )
        sys.exit()

    print(f"\n{colors['white']}{current_path}{colors['reset']}")
    for variant in list_of_folders(current_path):
        process_variant(variant)
    if "mfu" in current_path and not store:
        # Print - 30 times
        print(f"\n{colors['white']}{'-' * 30}{colors['reset']}")
        free_slots = slots()
        if free_slots:
            exe = os.environ["PROJECT"]
            last_job_file = (
                f"/home/ulc/ba/mfu/code/{exe}/results/last_submitted_job.tmp"
            )
            if os.path.isfile(last_job_file):
                print(
                    f"\n{colors['bold']}Submit {colors['cyan']}{free_slots}{colors['reset']}"
                    + f"{colors['bold']} jobs{colors['reset']} {ask['yesno']} ",
                    end="",
                )
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
