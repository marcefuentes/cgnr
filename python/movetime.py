#! /usr/bin/env python

import os

input_extension = ".gl2"
output_extension = ".glo"

for c in range(101, 542):
    input_file = f"{c}{input_extension}"
    output_file = f"{c}{output_extension}"
    if os.path.isfile(input_file):
        with open(input_file, "r") as f:
            line = f.readline()
            while line:
                if line.startswith("TimeElapsed"):
                    time = line
                    break
                line = f.readline()
        with open(output_file, "r") as f:
            content = f.read()
        with open(output_file, "w") as f:
            f.write(content)
            f.write(time)
        os.remove(input_file)
