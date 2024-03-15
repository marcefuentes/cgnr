#! /usr/bin/env python

import argparse
import csv
import os
import sys

import tools.colors as cc
from slurm.get_config import get_config
from slurm.tools import get_running_jobs
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

def process_variant(path, number_of_lines, input_file_extension, output_file_extension, tsml):

    folder_dict = {}

    variant = path.split("/")[-1]
    if os.path.islink(path):
        print(f"{cc.bold}{cc.red}{variant}{cc.reset_format}")
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

    mechanisms = list_of_folders(path)
    for mechanism in mechanisms:
        tsml = process_mechanism(mechanism, folder_dict, number_of_lines, input_file_extension, output_file_extension, tsml)
    return tsml

def process_mechanism(path, folder_dict, number_of_lines, input_file_extension, output_file_extension, tsml):

    mechanism = path.split("/")[-1]
    if os.path.islink(path):
        print(f"{cc.bold}{cc.red}{mechanism}{cc.reset_format}", end = "")
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

    givens = list_of_folders(path)
    for given in givens:
        tsml = process_given(given, folder_dict, number_of_lines, input_file_extension, output_file_extension, tsml)
    return tsml

def process_given(path, folder_dict, number_of_lines, input_file_extension, output_file_extension, tsml):
    
    given = path.split("/")[-1]
    if os.path.islink(path):
        print(f"{cc.bold}{cc.red}\t{given}{cc.reset_format}", end = "  ")
    else:
        print(f"{cc.bold}\t{given}{cc.reset_format}", end = "  ")

    folder_dict["Given"] = float(given[-3:]) / 100

    input_files = [f for f in os.listdir(path) if f.endswith(input_file_extension)]
    total_files = len(input_files)
    if total_files == 0:
        print(f"{cc.bold}{cc.red}no {input_file_extension[1:]} files{cc.reset_format}")
        return
    with open(os.path.join(path, input_files[0]), "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = row
            if key == "Given":
                if float(value) != folder_dict[key]:
                    print(f"{cc.bold}{cc.red}{key} {folder_dict[key]} {value}{cc.reset_format}", end = " ")
            elif key in folder_dict:
                if int(value) != folder_dict[key]:
                    print(f"{cc.bold}{cc.red}{key} {folder_dict[key]} {value}{cc.reset_format}", end = " ")
    f_smaller_number_of_lines = 0
    f_equal_number_of_lines = 0
    f_larger_number_of_lines = 0
    for f in os.listdir(path):
        if f.endswith(output_file_extension):
            output_file = os.path.join(path, f)
            with open(output_file, "r") as output:
                lines = output.readlines()
                if len(lines) < number_of_lines:
                    f_smaller_number_of_lines += 1
                elif len(lines) == number_of_lines:
                    f_equal_number_of_lines += 1
                elif len(lines) > number_of_lines:
                    f_larger_number_of_lines += 1
    tsml += f_smaller_number_of_lines
    notstarted = total_files - f_smaller_number_of_lines - f_equal_number_of_lines - f_larger_number_of_lines
    print(f"{cc.bold}{cc.green if f_equal_number_of_lines else cc.reset_format}{f_equal_number_of_lines:>4}{cc.reset_format}" if f_equal_number_of_lines else "", end = "")
    print(f"{cc.bold}{cc.yellow if f_smaller_number_of_lines else cc.reset_format}{f_smaller_number_of_lines:>4}{cc.reset_format}" if f_smaller_number_of_lines else "", end = "")
    print(f"{cc.bold}{cc.red if notstarted else cc.reset_format}{notstarted:>4}{cc.reset_format}" if notstarted else "", end = "")
    print(f"{cc.bold}{cc.blue if f_larger_number_of_lines else cc.reset_format}{f_larger_number_of_lines:>4}{cc.reset_format}" if f_larger_number_of_lines else "", end = "")
    if f_smaller_number_of_lines:
        running_jobs = get_running_jobs(path.split("/")[-2])
        dead_jobs = f_smaller_number_of_lines - running_jobs
        print(f"{cc.bold}{cc.greyred if dead_jobs else cc.reset_format}{dead_jobs:>4}{cc.reset_format}" if dead_jobs else "", end = "")
    print()
    return tsml

def main():

    exe = get_config_value("exe")
    number_of_lines = get_config("number_of_lines")
    input_file_extension = get_config("input_file_extension")
    output_file_extension = get_config("first_output_file_extension")

    mypath = get_results_path(use_store=args.store, exe=exe)

    if os.path.isdir(mypath):
        os.chdir(mypath)
    else:
        print(f"{cc.bold}{cc.red}Directory {mypath} does not exist{cc.reset_format}")
        exit()

    print(f"\n{cc.bold}{mypath}{cc.reset_format}")
    tsml = 0
    variants = list_of_folders(mypath)
    for variant in variants:
        tsml = process_variant(variant, number_of_lines, input_file_extension, output_file_extension, tsml)
    print(f"\n{cc.bold}Total unfinished: {cc.yellow}{tsml}{cc.reset_format}\n" if tsml else "")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Status of tasks",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # It admits only one argument, which is optional and can only be "store"
    parser.add_argument("store", nargs="?", default="no", help="store (optional): use store instead of home (only in cesga)")
    args = parser.parse_args()
    main()
