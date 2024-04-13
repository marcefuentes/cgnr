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
    default_groupsize = get_config("GroupSize")
    parser.add_argument(
        "--groupsize",
        type=int,
        default=default_groupsize,
        help="group size (default={default_groupsize})"
    )
    default_cost = get_config("Cost")
    parser.add_argument(
        "--cost",
        type=float,
        default=default_cost,
        help="cost value (default={default_cost})"
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
    default_given = get_config("Given")
    parser.add_argument(
        "--given",
        type=float,
        default=default_given,
        help=f"given value (default={default_given})"
    )
    return parser.parse_args()

def main():
    """Main function"""

    args = parse_args()

    if args.language == 1:
        variant = "lang_"
    else:
        variant = "nolang_"
    if args.shuffle == 1:
        variant = f"{variant}shuffle_"
    else:
        variant = f"{variant}noshuffle_"
    cost_str = str(-int(args.cost))
    variant = f"{variant}cost{cost_str}_"
    groupsize_str = str(pow(2, args.groupsize))
    variant = f"{variant}{groupsize_str}"

    mechanism = ""
    if args.partnerchoice == 1:
        mechanism = "p"

    reciprocity = 0
    if args.indirectr == 1:
        reciprocity = 1
        mechanism = f"{mechanism}i"

    if args.partnerchoice == 0 and args.indirectr == 0:
        mechanism = "none"

    given_str = str(int((args.given) * 100)).zfill(3)
    path = f"{variant}/{mechanism}/given{given_str}"
    os.makedirs(path, exist_ok=True)

    alpha_min = get_config("alpha_min")
    alpha_max = get_config("alpha_max")
    loges_min = get_config("loges_min")
    loges_max = get_config("loges_max")
    grid = get_config("grid")
    alphas = np.linspace(alpha_min, alpha_max, grid)
    logess = np.linspace(loges_min, loges_max, grid)

    input_file_extension = get_config("input_file_extension")
    c = 101

    standard_params = {
        "Seed": 1,
        "N": get_config("N"),
        "Runs": get_config("Runs"),
        "Time": get_config("Time"),
        "Periods": get_config("Periods"),
        "qBMutationSize": get_config("qBMutationSize"),
        "GrainMutationSize": get_config("GrainMutationSize"),
        "DeathRate": get_config("DeathRate")
    }

    for alpha in alphas:
        for loges in logess:
            filename = f"{path}/{c}{input_file_extension}"
            with open(filename, "w", encoding="utf-8") as f:
                for key, value in standard_params.items():
                    f.write(f"{key},{value}\n")
                f.write(f"GroupSize,{args.groupsize}\n")
                f.write(f"Cost,{args.cost}\n")
                f.write(f"PartnerChoice,{args.partnerchoice}\n")
                f.write(f"Reciprocity,{reciprocity}\n")
                f.write(f"IndirectR,{args.indirectr}\n")
                f.write(f"Language,{args.language}\n")
                f.write(f"Shuffle,{args.shuffle}\n")
                f.write(f"alpha,{alpha:.6}\n")
                f.write(f"logES,{loges}\n")
                f.write(f"Given,{args.given}\n")
            c = c + 1

if __name__ == "__main__":
    main()
