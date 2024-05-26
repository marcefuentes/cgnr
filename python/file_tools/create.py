#!/usr/bin/env python

"""Create input files for the simulations"""

import os
import numpy as np

from common_modules.settings import SETTINGS as settings
from modules_create.parse_args import parse_args


def main(args):
    """Main function"""

    input_file_extension = settings["input_file_extension"]
    counter = 101

    if args.language == 1:
        path = "lang_"
    else:
        path = "nolang_"

    path += f"{'shuffle_' if args.shuffle else 'noshuffle_'}"
    path += f"cost{str(-int(args.cost))}_"
    path += f"{str(pow(2, args.groupsize))}/"

    if args.partnerchoice:
        path += "p"
    reciprocity = 0
    if args.directr:
        reciprocity = 1
        path += "d"
    if args.indirectr:
        reciprocity = 1
        path += "i"
    if not args.partnerchoice and not reciprocity:
        path += "none"

    path += f"/{str(args.given)}"
    os.makedirs(path, exist_ok=True)

    grid = settings["grid"]
    alphas = np.linspace(settings["alpha_min"], settings["alpha_max"], grid)
    logess = np.linspace(settings["loges_min"], settings["loges_max"], grid)

    standard_params = {
        "Seed": 1,
        "N": settings["N"],
        "Runs": settings["Runs"],
        "Time": settings["Time"],
        "Periods": settings["Periods"],
        "qBMutationSize": settings["qBMutationSize"],
        "GrainMutationSize": settings["GrainMutationSize"],
        "DeathRate": settings["DeathRate"],
    }

    for alpha in alphas:
        for loges in logess:
            filename = f"{path}/{counter}{input_file_extension}"
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
            counter = counter + 1


if __name__ == "__main__":
    parsed_args = parse_args("Create input files for simulations")
    main(parsed_args)
