#! /usr/bin/env python

import csv
import os
import sys

import mycolors as c

nlines = 10
input_file_extension = ".glo"
output_file_extension = ".csv"

if len(sys.argv) > 1:
    if os.path.isdir(sys.argv[1]):
        os.chdir(sys.argv[1])
    else:
        print(f"{c.red}Directory {sys.argv[1]} does not exist{c.reset_format}")
        exit()

folder_dict = {}
folder_dict["DeathRate"] = -7
folder_dict["Shuffle"] = 0
folder_dict["Language"] = 0

# get the name, not the full path, of the current folder

current_folder = os.getcwd()
variant = current_folder.split("/")[-1]
if "noshuffle" not in variant:
    folder_dict["Shuffle"] = 1
if "_d" in variant:
    folder_dict["DeathRate"] = -3
if "lang" in variant:
    folder_dict["Language"] = 1
cost_index = variant.find("cost")
cost = variant[cost_index + 4:cost_index + 6]
folder_dict["Cost"] = -int(cost)

mechanisms = [f for f in os.listdir(current_folder) if os.path.isdir(f)]
mechanisms.sort()
for mechanism in mechanisms:
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
    if "_128" in variant or "128" in mechanism:
        folder_dict["GroupSize"] = 7
    elif "_16" in variant or "16" in mechanism:
        folder_dict["GroupSize"] = 4
    elif "_8" in variant or "8" in mechanism:
        folder_dict["GroupSize"] = 3
    else:
        folder_dict["GroupSize"] = 2
    givens = [f for f in os.listdir(mechanism) if os.path.isdir(os.path.join(mechanism, f))]
    if len(givens) == 0:
        print(f"{c.red}empty{c.reset_format}")
        continue
    givens.sort()
    for given in givens:
        folder_dict["Given"] = float(given[-3:]) / 100
        given_path = os.path.join(mechanism, given)
        input_files = [f for f in os.listdir(given_path) if f.endswith(input_file_extension)]
        print(f"{c.cyan}{mechanism}{c.reset_format}\t{c.blue}{given}{c.reset_format}", end = "  ")
        total_files = len(input_files)
        if total_files == 0:
            print(f"{c.red}no {input_file_extension[1:]} files{c.reset_format}")
            continue
        with open(os.path.join(given_path, input_files[0]), "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                key, value = row
                if key == "Given":
                    if float(value) != folder_dict[key]:
                        print(f"{c.red}{key} {folder_dict[key]} {value}{c.reset_format}", end = " ")
                elif key in folder_dict:
                    if int(value) != folder_dict[key]:
                        print(f"{c.red}{key} {folder_dict[key]} {value}{c.reset_format}", end = " ")
        f_smaller_nlines = 0
        f_equal_nlines = 0
        f_larger_nlines = 0
        for f in os.listdir(given_path):
            if f.endswith(output_file_extension):
                output_file = os.path.join(given_path, f)
                with open(output_file, "r") as output:
                    lines = output.readlines()
                    if len(lines) < nlines:
                        f_smaller_nlines += 1
                    elif len(lines) == nlines:
                        f_equal_nlines += 1
                    elif len(lines) > nlines:
                        f_larger_nlines += 1
        notstarted = total_files - f_smaller_nlines - f_equal_nlines - f_larger_nlines
        print(f"{c.green if f_equal_nlines else c.reset_format}{f_equal_nlines:>4}{c.reset_format}" if f_equal_nlines else "", end = "")
        print(f"{c.yellow if f_smaller_nlines else c.reset_format}{f_smaller_nlines:>4}{c.reset_format}" if f_smaller_nlines else "", end = "")
        print(f"{c.red if notstarted else c.reset_format}{notstarted:>4}{c.reset_format}" if notstarted else "", end = "")
        print(f"{c.red if f_larger_nlines else c.reset_format}{f_larger_nlines:>4}{c.reset_format}" if f_larger_nlines else "", end = "")
        if f_larger_nlines:
            print(f"> {nlines} lines{c.reset_format}")
        print()
