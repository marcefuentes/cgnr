#! /usr/bin/env python

import csv
import os
import sys

import mycolors as c

class Config:
    def __init__(self, nlines, input_file_extension, output_file_extension):
        self.nlines = nlines
        self.input_file_extension = input_file_extension
        self.output_file_extension = output_file_extension

def parse_folder_name(folder_name):
    folder_dict = {}
    folder_dict["DeathRate"] = -7
    folder_dict["Shuffle"] = 0
    folder_dict["Language"] = 0
    folder_dict["PartnerChoice"] = 0
    folder_dict["Reciprocity"] = 0
    folder_dict["IndirectR"] = 0
    folder_dict["GroupSize"] = 0
    folder_dict["Given"] = 0
    folder_dict["Cost"] = 0
    if "noshuffle" not in folder_name:
        folder_dict["Shuffle"] = 1
    if "_d" in folder_name:
        folder_dict["DeathRate"] = -3
    if "lang" in folder_name:
        folder_dict["Language"] = 1
    cost_index = folder_name.find("cost")
    cost = folder_name[cost_index + 4:cost_index + 6]
    folder_dict["Cost"] = -int(cost)
    if "p" in folder_name:
        folder_dict["PartnerChoice"] = 1
    if "i" in folder_name:
        folder_dict["Reciprocity"] = 1
        folder_dict["IndirectR"] = 1
    elif "r" in folder_name:
        folder_dict["Reciprocity"] = 1
        folder_dict["IndirectR"] = 0
    if "_128" in folder_name:
        folder_dict["GroupSize"] = 7
    elif "_16" in folder_name:
        folder_dict["GroupSize"] = 4
    elif "_8" in folder_name:
        folder_dict["GroupSize"] = 3
    else:
        folder_dict["GroupSize"] = 2
    folder_dict["Given"] = float(folder_name[-3:]) / 100
    return folder_dict

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
        folder_dict["Given"] = float(given[-3:]) / 100
        given_path = os.path.join(mechanism, given)
        input_files = [f for f in os.listdir(given_path) if f.endswith(input_file_extension)]
        print(f"{c.white}{mechanism}{c.reset_format}\t{c.white}{given}{c.reset_format}", end = "  ")
        total_files = len(input_files)
        if total_files == 0:
            print(f"{c.bold}{c.red}no {input_file_extension[1:]} files{c.reset_format}")
            continue
        with open(os.path.join(given_path, input_files[0]), "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                key, value = row
                if key == "Given":
                    if float(value) != folder_dict[key]:
                        print(f"{c.bold}{c.red}{key} {folder_dict[key]} {value}{c.reset_format}", end = " ")
                elif key in folder_dict:
                    if int(value) != folder_dict[key]:
                        print(f"{c.bold}{c.red}{key} {folder_dict[key]} {value}{c.reset_format}", end = " ")
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
        print(f"{c.bold}{c.green if f_equal_nlines else c.reset_format}{f_equal_nlines:>4}{c.reset_format}" if f_equal_nlines else "", end = "")
        print(f"{c.bold}{c.yellow if f_smaller_nlines else c.reset_format}{f_smaller_nlines:>4}{c.reset_format}" if f_smaller_nlines else "", end = "")
        print(f"{c.bold}{c.red if notstarted else c.reset_format}{notstarted:>4}{c.reset_format}" if notstarted else "", end = "")
        print(f"{c.bold}{c.blue if f_larger_nlines else c.reset_format}{f_larger_nlines:>4}{c.reset_format}" if f_larger_nlines else "", end = "")
        print()

def main():
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            os.chdir(sys.argv[1])
        else:
            print(f"{c.bold}{c.red}Directory {sys.argv[1]} does not exist{c.reset_format}")
            exit()

    nlines = 10
    input_file_extension = ".glo"
    output_file_extension = ".csv"

    # get the name, not the full path, of the current folder

    current_folder = os.getcwd()
    variant = current_folder.split("/")[-1]
    
    mechanisms = [f for f in os.listdir(current_folder) if os.path.isdir(f)]
    mechanisms.sort()
    for mechanism in mechanisms:
        givens = [f for f in os.listdir(mechanism) if os.path.isdir(os.path.join(mechanism, f))]
        if len(givens) == 0:
            print(f"{c.bold}{c.red}empty{c.reset_format}")
            continue
        givens.sort()
        for given in givens:
            folder_dict.update(parse_folder_name(os.path.join(current_folder, mechanism)))
            folder_dict["Given"] = float(given[-3:]) / 100
            process_given_directory(os.path.join(mechanism, given), folder_dict.copy(), nlines, input_file_extension, output_file_extension)

if __name__ == "__main__":
    main()
