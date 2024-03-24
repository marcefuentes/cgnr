#!/usr/bin/env python

import argparse
import csv
import os
import sys

import tools.colors as cc
from slurm.get_config import get_config
from slurm.tools import get_squeue_stats
from tools.list_of_folders import list_of_folders

def get_results_path(use_store=False):
    exe = get_config("exe")
    if use_store != "no":
        store_path = os.environ.get("STORE")
        if store_path is None:
            raise ValueError("STORE environment variable not set")
        return f"{store_path}/code/{exe}/results"
    else:
        home_path = os.environ.get("HOME")
        return f"{home_path}/code/{exe}/results"

def process_variant(current_path, total_pending, total_running):

    folder_dict = {}

    variant = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{cc.cyan}{variant}{cc.reset}")
    else:
        print(f"\n{cc.white}{variant}{cc.reset}")

    if "noshuffle" not in variant:
        folder_dict["Shuffle"] = 1
    else:
        folder_dict["Shuffle"] = 0
    if "_d" in variant:
        folder_dict["DeathRate"] = -3
    else:
        folder_dict["DeathRate"] = -7
    if "lang" in variant:
        folder_dict["Language"] = 1
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
        total_pending, total_running = process_mechanism(mechanism, folder_dict, total_pending, total_running)
    return total_pending, total_running

def process_mechanism(current_path, folder_dict, total_pending, total_running):

    mechanism = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{cc.cyan}{mechanism}{cc.reset}", end = "")
    else:
        print(f"{cc.white}{mechanism}{cc.reset}", end = "")

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
        total_pending, total_running = process_given(given, folder_dict, total_pending, total_running)
    return total_pending, total_running

def process_given(current_path, folder_dict, total_pending, total_running):
    
    number_of_lines = get_config("number_of_lines")
    input_file_extension = get_config("input_file_extension")
    output_file_extension = get_config("output_file_extension_0")

    current_path_folders = current_path.split("/")
    given = current_path_folders[-1]
    if os.path.islink(current_path):
        print(f"{cc.cyan}\t{given}{cc.reset}", end = "  ")
    else:
        print(f"{cc.white}\t{given}{cc.reset}", end = "  ")

    folder_dict["Given"] = float(given[-3:]) / 100

    input_files = [f for f in os.listdir(current_path) if f.endswith(input_file_extension)]
    total_jobs = len(input_files)
    if total_jobs == 0:
        print(f"{cc.bold}{cc.red}no {input_file_extension[1:]} files{cc.reset}")
        return
    with open(os.path.join(current_path, input_files[0]), "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = row
            if key == "Given":
                if float(value) != folder_dict[key]:
                    print(f"{cc.bold}{cc.red}{key} {folder_dict[key]} {value}{cc.reset}", end = " ")
            elif key in folder_dict:
                if int(value) != folder_dict[key]:
                    print(f"{cc.bold}{cc.red}{key} {folder_dict[key]} {value}{cc.reset}", end = " ")

    finished_jobs = 0
    garbled_jobs = 0
    no_header = 0
    one_line_jobs = 0

    output_files = [f for f in os.listdir(current_path) if f.endswith(output_file_extension)]
    for output_file in output_files:
        with open(os.path.join(current_path, output_file), "r") as f:
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
    if "mfu" in current_path:
        running_jobs = get_squeue_stats("name", jobname, "running")
        pending_jobs = get_squeue_stats("name", jobname, "pending")
    else:
        running_jobs = 0
        pending_jobs = 0
    dead_jobs = one_line_jobs - running_jobs
    to_submit_jobs = total_jobs - pending_jobs - running_jobs - finished_jobs - garbled_jobs - no_header - dead_jobs

    total_pending += pending_jobs
    total_running += running_jobs
    print(f"{cc.bold}{cc.green}{finished_jobs:>4}{cc.reset}" if finished_jobs else   "", end = "")
    print(f"{cc.bold}{cc.yellow}{running_jobs:>4}{cc.reset}" if running_jobs else    "", end = "")
    print(f"{cc.bold}{cc.white}{pending_jobs:>4}{cc.reset}"  if pending_jobs else    "", end = "")
    print(f"{cc.bold}{cc.grey}{to_submit_jobs:>4}{cc.reset}" if to_submit_jobs else  "", end = "")
    print(f"{cc.bold}{cc.red}{dead_jobs:>4}{cc.reset}"       if dead_jobs else       "", end = "")
    print(f"{cc.bold}{cc.purple}{no_header:>4}{cc.reset}"    if no_header else       "", end = "")
    print(f"{cc.bold}{cc.blue}{garbled_jobs:>4}{cc.reset}"   if garbled_jobs else    "", end = "")
    print()
    return total_pending, total_running

def main():

    queues = [get_config("queue_0"), get_config("queue_1")]
    current_path = get_results_path(use_store=args.store)

    if os.path.isdir(current_path):
        os.chdir(current_path)
    else:
        print(f"{cc.bold}{cc.red}Directory {current_path} does not exist{cc.reset}")
        exit()

    print(f"\n{cc.white}{current_path}{cc.reset}")
    total_pending = 0
    total_running = 0
    variants = list_of_folders(current_path)
    for variant in variants:
        total_pending, total_running = process_variant(variant, total_pending, total_running)
    if "mfu" in current_path:
        print(f"\nTotal: {cc.yellow}{total_running:>15}{cc.reset}{total_pending:>4}")
        total_pending = 0
        total_running = 0
        for queue in queues:
            total_pending += get_squeue_stats("qos", queue, "pending")
            total_running += get_squeue_stats("qos", queue, "running")
        print(f"Total (by queue): {cc.yellow}{total_running:>4}{cc.reset}{total_pending:>4}\n")
    else:
        print()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Status of tasks",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # It admits only one argument, which is optional and can only be "store"
    parser.add_argument("store", nargs="?", default="no", help="store (optional): use store instead of home (only in cesga)")
    args = parser.parse_args()
    main()
