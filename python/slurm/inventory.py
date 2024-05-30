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
    base_path = os.environ.get("STORE" if store else "HOME")
    if base_path is None:
        raise ValueError(f"{'STORE' if store else 'HOME'} environment variable not set")
    return os.path.join(base_path, "code", exe, "results")


def job_status(current_path, total_jobs):
    """Find status of jobs in a given folder."""

    output_file_extension = project["output_file_extensions"][0]
    status_counts = {
        "finished": 0,
        "garbled": 0,
        "no_header": 0,
        "one_line": 0,
    }

    for output_file in os.listdir(current_path):
        if output_file.endswith(output_file_extension):
            with open(os.path.join(current_path, output_file), "r", encoding="utf-8") as f:
                n_lines = sum(1 for line in f)
                if n_lines == project["number_of_lines"]:
                    status_counts["finished"] += 1
                elif n_lines == 1:
                    status_counts["one_line"] += 1
                elif n_lines == project["number_of_lines"] - 1:
                    status_counts["no_header"] += 1
                else:
                    status_counts["garbled"] += 1
    
    job_name = f"{current_path.split('/')[-2]}"
    job_name += f"_{current_path.split('/')[-1]}"
    job_name += f"_{current_path.split('/')[-3]}"
    running_jobs = get_squeue_stats("name", job_name, "running") if "mfu" in current_path and "Store" not in current_path else 0
    pending_jobs = get_squeue_stats("name", job_name, "pending") if "mfu" in current_path and "Store" not in current_path else status_counts["one_line"]
    dead_jobs = status_counts["one_line"] - running_jobs if "mfu" in current_path and "Store" not in current_path else 0
    to_submit_jobs = total_jobs - status_counts["finished"] - status_counts["garbled"] - status_counts["no_header"] - running_jobs - pending_jobs - dead_jobs
    status_output = [
        (colors["green"], status_counts["finished"]),
        (colors["yellow"], running_jobs),
        (colors["white"], pending_jobs),
        (colors["grey"], to_submit_jobs),
        (colors["red"], dead_jobs),
        (colors["purple"], status_counts["no_header"]),
        (colors["blue"], status_counts["garbled"]),
    ]

    for color, count in status_output:
        if count:
            print(f"{colors['bold']}{color}{count:>4}{colors['reset']}", end="")
    print()


def process_given_folder(current_path, folder_data):
    """Process a given folder."""

    given = current_path.split("/")[-1]

    print(f"{colors['cyan'] if os.path.islink(current_path) else colors['white']}\t{given:<5}{colors['reset']}", end="")

    input_files = [
        f for f in os.listdir(current_path) if f.endswith(project["input_file_extension"])
    ]

    if not input_files:
        print(
            f"{colors['bold']}{colors['red']}no {project['input_file_extension'][1:]} files{colors['reset']}"
        )
        return

    find_errors(current_path, input_files[0], folder_data)
    job_status(current_path, len(input_files))


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
        process_given_folder(given, folder_data)


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
