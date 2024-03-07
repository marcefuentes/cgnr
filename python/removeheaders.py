#! /usr/bin/env python

import os

extensions = [".csv", ".frq"]
number_of_lines_to_keep = 10  # Use a descriptive variable name

def delete_first_line_if_file_has_11_lines(filename):
    if not os.path.isfile(filename):
        return  # Skip non-existent files

    with open(filename, "r") as f:
        line_count = sum(1 for line in f)

    if line_count != number_of_lines_to_keep + 1:
        return  # Skip files with incorrect line count

    with open(filename, "r") as f:
        lines = f.readlines()

    with open(filename, "w") as f:
        f.writelines(lines[1:])

for c in range(101, 542):
    for extension in extensions:
        filename = f"{c}{extension}"
        delete_first_line_if_file_has_11_lines(filename)

