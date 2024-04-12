#!/usr/bin/env python

"""Create input files for the simulations"""

import argparse
import math
import os
import numpy as np

from common_modules.get_config import get_config

def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--groupsize",
        type=int,
        default=4,
        help="group size (default=4)"
    )
    parser.add_argument(
        "--cost",
        type=float,
        default=15,
        help="cost value (default=15)"
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
        default="100",
        help="given value (default=100)"
    )
    return parser.parse_args()

def main():
    """Main function"""

    input_file_extension = get_config("input_file_extension")
    alpha_min = get_config("alpha_min")
    alpha_max = get_config("alpha_max")
    loges_min = get_config("loges_min")
    loges_max = get_config("loges_max")

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
    cost_str = str(args.cost)
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
    alphas = np.linspace(alpha_min, alpha_max, num)
    logess = np.linspace(loges_min, loges_max, num)
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
            filename = f"{path}/{c}{input_file_extension}"
            with open(filename, "w", encoding="utf-8") as f:
                for key, value in standard_params.items():
                    f.write(f"{key},{value}\n")
                f.write(f"GroupSize,{groupsize}\n")
                f.write(f"Cost,{-args.cost}\n")
                f.write(f"PartnerChoice,{args.partnerchoice}\n")
                f.write(f"Reciprocity,{reciprocity}\n")
                f.write(f"IndirectR,{args.indirectr}\n")
                f.write(f"Language,{args.language}\n")
                f.write(f"Shuffle,{args.shuffle}\n")
                f.write(f"alpha,{alpha:.6}\n")
                f.write(f"logES,{loges}\n")
                f.write(f"Given,{given}\n")
            c = c + 1

if __name__ == "__main__":
    main()
