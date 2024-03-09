#! /usr/bin/env python

import csv
import os
import sys

import mycolors as c
from myget_config import get_config
from mylist_of_folders import list_of_folders

def get_config_value(variable):
    try:
        return get_config(variable)
    except RuntimeError as e:
        print(f"{c.bold}{c.red}Error getting config value '{variable}': {e}{c.reset_format}")
        exit(1)

def parse_path(folder_dict, path):
    folder_dict["DeathRate"] = -7
    folder_dict["Shuffle"] = 0
    folder_dict["Language"] = 0
    folder_dict["PartnerChoice"] = 0
    folder_dict["Reciprocity"] = 0
    folder_dict["IndirectR"] = 0
    folder_dict["GroupSize"] = 2
    folder_dict["Given"] = 0
    folder_dict["Cost"] = 0
    path_folders = path.split("/")
    variant = path_folders[-3]
    if "noshuffle" not in variant:
        folder_dict["Shuffle"] = 1
    if "_d" in variant:
        folder_dict["DeathRate"] = -3
    if "lang" in variant:
        folder_dict["Language"] = 1
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
    folder_dict["Given"] = float(variant[-3:]) / 100
    mechanism = path_folders[-2]
    if "p" in mechanism:
        folder_dict["PartnerChoice"] = 1
    if "i" in mechanism:
        folder_dict["Reciprocity"] = 1
        folder_dict["IndirectR"] = 1
    elif "r" in mechanism:
        folder_dict["Reciprocity"] = 1
        folder_dict["IndirectR"] = 0
    given = path_folders[-1]
    folder_dict["Given"] = float(given[-3:]) / 100
    return folder_dict

def process_folder(given, number_of_lines, input_file_extension, output_file_extension):
    folder_dict = {}
    folder_dict = parse_path(folder_dict, given)
    input_files = [f for f in os.listdir(given) if f.endswith(input_file_extension)]
    path_folders = given.split("/")
    mechanism = path_folders[-2]
    given_print = path_folders[-1]
    print(f"{c.white}{mechanism}{c.reset_format}\t{c.white}{given_print}{c.reset_format}", end = "  ")
    total_files = len(input_files)
    if total_files == 0:
        print(f"{c.bold}{c.red}no {input_file_extension[1:]} files{c.reset_format}")
        return
    with open(os.path.join(given, input_files[0]), "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = row
            if key == "Given":
                if float(value) != folder_dict[key]:
                    print(f"{c.bold}{c.red}{key} {folder_dict[key]} {value}{c.reset_format}", end = " ")
            elif key in folder_dict:
                if int(value) != folder_dict[key]:
                    print(f"{c.bold}{c.red}{key} {folder_dict[key]} {value}{c.reset_format}", end = " ")
    f_smaller_number_of_lines = 0
    f_equal_number_of_lines = 0
    f_larger_number_of_lines = 0
    for f in os.listdir(given):
        if f.endswith(output_file_extension):
            output_file = os.path.join(given, f)
            with open(output_file, "r") as output:
                lines = output.readlines()
                if len(lines) < number_of_lines:
                    f_smaller_number_of_lines += 1
                elif len(lines) == number_of_lines:
                    f_equal_number_of_lines += 1
                elif len(lines) > number_of_lines:
                    f_larger_number_of_lines += 1
    notstarted = total_files - f_smaller_number_of_lines - f_equal_number_of_lines - f_larger_number_of_lines
    print(f"{c.bold}{c.green if f_equal_number_of_lines else c.reset_format}{f_equal_number_of_lines:>4}{c.reset_format}" if f_equal_number_of_lines else "", end = "")
    print(f"{c.bold}{c.yellow if f_smaller_number_of_lines else c.reset_format}{f_smaller_number_of_lines:>4}{c.reset_format}" if f_smaller_number_of_lines else "", end = "")
    print(f"{c.bold}{c.red if notstarted else c.reset_format}{notstarted:>4}{c.reset_format}" if notstarted else "", end = "")
    print(f"{c.bold}{c.blue if f_larger_number_of_lines else c.reset_format}{f_larger_number_of_lines:>4}{c.reset_format}" if f_larger_number_of_lines else "", end = "")
    print()

def main():
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            os.chdir(sys.argv[1])
        else:
            print(f"{c.bold}{c.red}Directory {sys.argv[1]} does not exist{c.reset_format}")
            exit()

    exe = get_config_value("exe")
    number_of_lines = get_config("number_of_lines")
    input_file_extension = get_config("input_file_extension")
    output_file_extension = get_config("first_output_file_extension")

    current_folder = os.getcwd()
    mechanisms = list_of_folders(current_folder)

    for mechanism in mechanisms:
        givens = list_of_folders(mechanism)
        for given in givens:
            process_folder(given,
                           number_of_lines,
                           input_file_extension,
                           output_file_extension)

if __name__ == "__main__":
    main()
