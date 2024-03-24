#!/usr/bin/env python

import numpy as np
import os
import sys

import slurm.get_config as get_config

# the script accepts exactly three arguments
if len(sys.argv) != 4:
    print("Usage: python create.py <variant> <mechanism> <given>")
    sys.exit()

variant = sys.argv[1]
mechanism = sys.argv[2]
given = sys.argv[3]

output_file_extension = get_config("input_file_extension")

if "_d" in variant:
    deathrate = -3
else:
    deathrate = -7

if "128" in variant or "128" in mechanism:
    groupsize = 7
elif "16" in variant or "16" in mechanism:
    groupsize = 4
elif "8" in variant or "8" in mechanism:
    groupsize = 3
else:
    groupsize = 2

if "p" in mechanism:
    partnerchoice = 1
else:
    partnerchoice = 0

if "i" in mechanism:
    reciprocity = 1
    indirectr = 1
elif "r" in mechanism:
    reciprocity = 1
    indirectr = 0
else:
    reciprocity = 0
    indirectr = 0

if "lang" in variant or "l" in mechanism:
    language = 1
else:
    language = 0

if "noshuffle" in variant:
    shuffle = 0
else:
    shuffle = 1

path = f"{variant}/{mechanism}/{given}"
os.makedirs(path, exist_ok=True)

num = 21
alphas = np.linspace(0.1, 0.9, num)
logess = np.linspace(-5.0, 5.0, num)
Given = float(given[-3:]) / 100
cost = -int(variant[variant.find("cost") + 4:variant.find("cost") + 6])

c = 101

for alpha in alphas:
    for loges in logess:
        filename = f"{path}/{c}{output_file_extension}"
        f = open(filename, "w")
        f.write("Seed,1\n")
        f.write("N,12\n")
        # standard Runs,30
        f.write("Runs,30\n")
        # standard Time,21
        f.write("Time,21\n")
        f.write("Periods,3\n")
        f.write("qBMutationSize,-6\n")
        f.write("GrainMutationSize,-6\n")
        f.write(f"DeathRate,{deathrate}\n")
        f.write(f"GroupSize,{groupsize}\n")
        f.write(f"Cost,{cost}\n")
        f.write(f"PartnerChoice,{partnerchoice}\n")
        f.write(f"Reciprocity,{reciprocity}\n")
        f.write(f"IndirectR,{indirectr}\n")
        f.write(f"Language,{language}\n")
        f.write(f"Shuffle,{shuffle}\n")
        f.write(f"alpha,{alpha:.6}\n")
        f.write(f"logES,{loges}\n")
        f.write(f"Given,{Given}\n")

        f.close()
        c = c + 1
