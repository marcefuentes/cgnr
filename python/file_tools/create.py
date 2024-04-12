#!/usr/bin/env python

import argparse
import math
import numpy as np
import os
import sys

from common_modules.get_config import get_config

def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--groupsize",
        type=int,
        default=4,
        help="group size"
    )
    parser.add_argument(
        "--cost",
        type=float,
        default=-15,
        help="cost value"
    )
    parser.add_argument(
        "--partnerchoice",
        action="store_const",
        const=1,
        default=0,
        help="Enable partnerchoice (1 if present)"
    )
    parser.add_argument(
        "--indirectr",
        action="store_const",
        const=1,
        default=0,
        help="Enable indirectr (1 if present)"
    )
    parser.add_argument(
        "--language",
        action="store_const",
        const=1,
        default=0,
        help="Enable language (1 if present)"
    )
    parser.add_argument(
        "--shuffle",
        action="store_const",
        const=1,
        default=0,
        help="Enable shuffle (1 if present)"
    )
    parser.add_argument(
        "--given",
        type=str,
        required=True,
        help="given value"
    )
    return parser.parse_args()

def main():
    """Main function"""

    INPUT_FILE_EXTENSION = get_config("input_file_extension")
    ALPHA_MIN = get_config("alpha_min")
    ALPHA_MAX = get_config("alpha_max")
    LOGES_MIN = get_config("loges_min")
    LOGES_MAX = get_config("loges_max")

    args = parse_args()
    reciprocity = 0

    if args.language == 1:
        variant = "lang_"
    else:
        variant = "nolang_"
    if args.shuffle == 1:
        variant = f"{variant}shuffle_"
    else:
        variant = f"{variant}noshuffle_"
    cost_str = str(abs(args.cost))
    variant = f"{variant}cost{cost_str}_"
    groupsize_str = str(args.groupsize)
    variant = f"{variant}{groupsize_str}"

    mechanism = ""
    if args.partnerchoice == 1:
        mechanism = "p"
    if args.indirectr == 1:
        reciprocity = 1
        mechanism = f"{mechanism}i"
    if args.partnerchoice == 0 and args.indirectr == 0:
        mechanism = "none"
    path = f"{variant}/{mechanism}/given{args.given}"
    os.makedirs(path, exist_ok=True)

    groupsize = int(math.log(args.groupsize)/math.log(2))
    given = float(args.given) / 100

    num = 21
    alphas = np.linspace(ALPHA_MIN, ALPHA_MAX, num)
    logess = np.linspace(LOGES_MIN, LOGES_MAX, num)
    standard_params = {
        "Seed": 1,
        "N": 12,
        "Runs": 30,
        "Time": 21,
        "Periods": 3,
        "qBMutationSize": -6,
        "GrainMutationSize": -6,
        "DeathRate": -7,
    }

    c = 101

    for alpha in alphas:
        for loges in logess:
            filename = f"{path}/{c}{INPUT_FILE_EXTENSION}"
            f = open(filename, "w")
            for key, value in standard_params.items():
                f.write(f"{key},{value}\n")
            f.write(f"GroupSize,{groupsize}\n")
            f.write(f"Cost,{args.cost}\n")
            f.write(f"PartnerChoice,{args.partnerchoice}\n")
            f.write(f"Reciprocity,{reciprocity}\n")
            f.write(f"IndirectR,{args.indirectr}\n")
            f.write(f"Language,{args.language}\n")
            f.write(f"Shuffle,{args.shuffle}\n")
            f.write(f"alpha,{alpha:.6}\n")
            f.write(f"logES,{loges}\n")
            f.write(f"Given,{given}\n")

            f.close()
            c = c + 1

if __name__ == "__main__":
    main()
