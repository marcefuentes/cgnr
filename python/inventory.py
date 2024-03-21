#!/usr/bin/env python

import argparse
import csv
import os
import sys

import tools.colors as cc
from slurm.get_config import get_config
from slurm.tools import submitted_job
from tools.list_of_folders import list_of_folders

def get_config_value(variable):
    try:
        return get_config(variable)
    except RuntimeError as e:
        print(f"{cc.bold}{cc.red}Error getting config value '{variable}': {e}{cc.reset_format}")
        exit(1)

def get_results_path(use_store=False, exe=None):

    if exe is None:
        raise ValueError("exe cannot be None")

    if use_store != "no":
        store_path = os.environ.get("STORE")
        if store_path is None:
            raise ValueError("STORE environment variable not set")
        return f"{store_path}/code/{exe}/results"
    else:
        home_path = os.environ.get("HOME")
        return f"{home_path}/code/{exe}/results"

def process_variant(current_path, number_of_lines, input_file_extension, output_file_extension, total_running):

    folder_dict = {}

    variant = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{cc.bold}{cc.red}->{variant}{cc.reset_format}")
    else:
        print(f"\n{cc.bold}{cc.cyan}{variant}{cc.reset_format}")

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
        total_running = process_mechanism(mechanism, folder_dict, number_of_lines, input_file_extension, output_file_extension, total_running)
    return total_running

def process_mechanism(current_path, folder_dict, number_of_lines, input_file_extension, output_file_extension, total_running):

    mechanism = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{cc.bold}{cc.red}->{mechanism}{cc.reset_format}", end = "")
    else:
        print(f"{cc.bold}{mechanism}{cc.reset_format}", end = "")

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
        total_running = process_given(given, folder_dict, number_of_lines, input_file_extension, output_file_extension, total_running)
    return total_running

def process_given(current_path, folder_dict, number_of_lines, input_file_extension, output_file_extension, total_running):
    
    given = current_path.split("/")[-1]
    if os.path.islink(current_path):
        print(f"{cc.bold}{cc.red}\t{given}{cc.reset_format}", end = "  ")
    else:
        print(f"{cc.bold}\t{given}{cc.reset_format}", end = "  ")

    folder_dict["Given"] = float(given[-3:]) / 100

    input_files = [f for f in os.listdir(current_path) if f.endswith(input_file_extension)]
    total_jobs = len(input_files)
    if total_jobs == 0:
        print(f"{cc.bold}{cc.red}no {input_file_extension[1:]} files{cc.reset_format}")
        return
    with open(os.path.join(current_path, input_files[0]), "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = row
            if key == "Given":
                if float(value) != folder_dict[key]:
                    print(f"{cc.bold}{cc.red}{key} {folder_dict[key]} {value}{cc.reset_format}", end = " ")
            elif key in folder_dict:
                if int(value) != folder_dict[key]:
                    print(f"{cc.bold}{cc.red}{key} {folder_dict[key]} {value}{cc.reset_format}", end = " ")
    to_submit_jobs = 0
    pending_jobs = 0
    running_jobs = 0
    finished_jobs = 0
    garbled_jobs = 0
    no_header = 0
    dead_jobs = 0

    mechanism = current_path.split("/")[-2]
    names = [name[:-4] for name in os.listdir(current_path) if name.endswith(input_file_extension)]
    for name in names:
        output_file = os.path.join(current_path, f"{name}{output_file_extension}")
        if os.path.isfile(output_file):
            with open(output_file, "r") as f:
                current_number_of_lines = sum(1 for line in f)
            if current_number_of_lines < number_of_lines - 1:
                if "mfu" in current_path and submitted_job(mechanism, name):
                    running_jobs += 1
                else:
                    dead_jobs += 1
            elif current_number_of_lines == number_of_lines - 1:
                no_header += 1
            elif current_number_of_lines == number_of_lines:
                finished_jobs += 1
            else:
                garbled_jobs += 1
        else:
            if "mfu" in current_path and submitted_job(mechanism, name):
                pending_jobs += 1
            else:
                to_submit_jobs += 1

    total_running += running_jobs
    print(f"{cc.bold}{cc.green}{finished_jobs:>4}{cc.reset_format}"    if finished_jobs else       "", end = "")
    print(f"{cc.bold}{cc.yellow}{running_jobs:>4}{cc.reset_format}"     if running_jobs else        "", end = "")
    print(f"{cc.bold}{cc.white}{pending_jobs:>4}{cc.reset_format}"     if pending_jobs else        "", end = "")
    print(f"{cc.bold}{cc.red}{to_submit_jobs:>4}{cc.reset_format}"   if to_submit_jobs else      "", end = "")
    print(f"{cc.bold}{cc.grey}{dead_jobs:>4}{cc.reset_format}"        if dead_jobs else           "", end = "")
    print(f"{cc.bold}{cc.purple}{no_header:>4}{cc.reset_format}"        if no_header else           "", end = "")
    print(f"{cc.bold}{cc.blue}{garbled_jobs:>4}{cc.reset_format}"     if garbled_jobs else        "", end = "")
    print()
    return total_running

def main():

    exe = get_config_value("exe")
    number_of_lines = get_config("number_of_lines")
    input_file_extension = get_config("input_file_extension")
    output_file_extension = get_config("first_output_file_extension")

    current_path = get_results_path(use_store=args.store, exe=exe)

    if os.path.isdir(current_path):
        os.chdir(current_path)
    else:
        print(f"{cc.bold}{cc.red}Directory {current_path} does not exist{cc.reset_format}")
        exit()

    print(f"\n{cc.bold}{current_path}{cc.reset_format}")
    total_running = 0
    variants = list_of_folders(current_path)
    for variant in variants:
        total_running = process_variant(variant, number_of_lines, input_file_extension, output_file_extension, total_running)
    if total_running and "mfu" in current_path:
        print(f"\n{cc.bold}Total running jobs: {cc.yellow}{total_running:>6}{cc.reset_format}\n" if total_running else "")
    else:
        print()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Status of tasks",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # It admits only one argument, which is optional and can only be "store"
    parser.add_argument("store", nargs="?", default="no", help="store (optional): use store instead of home (only in cesga)")
    args = parser.parse_args()
    main()
