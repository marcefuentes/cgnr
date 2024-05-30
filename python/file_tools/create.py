#!/usr/bin/env python

"""Create input files for the simulations"""

import os
import numpy as np

from modules_create.parse_args import parse_args
from settings_project.project import project


def main(args):
    """Main function"""

    input_file_extension = project["input_file_extension"]
    counter = 101

    path = "lang_" if args.language else "nolang_"
    path += "shuffle_" if args.shuffle else "noshuffle_"
    path += f"cost{str(-int(args.cost))}_"
    path += f"{str(pow(2, args.groupsize))}/"
    if not args.p and not args.d and not args.i:
        path += "none"
    else:
        path += "p" if args.p else ""
        path += "d" if args.d and not args.i else ""
        path += "i" if args.i else ""
    path += f"/{str(args.given)}"
    os.makedirs(path, exist_ok=True)

    standard_params = {
        "Seed": 1,
        "N": project["N"],
        "Runs": project["Runs"],
        "Time": project["Time"],
        "Periods": project["Periods"],
        "qBMutationSize": project["qBMutationSize"],
        "GrainMutationSize": project["GrainMutationSize"],
        "DeathRate": project["DeathRate"],
    }

    alphas = np.linspace(project["alpha_min"], project["alpha_max"], project["grid"])
    logess = np.linspace(project["loges_min"], project["loges_max"], project["grid"])
    reciprocity = 1 if args.d or args.i else 0

    for alpha in alphas:
        for loges in logess:
            filename = f"{path}/{counter}{input_file_extension}"
            with open(filename, "w", encoding="utf-8") as f:
                for key, value in standard_params.items():
                    f.write(f"{key},{value}\n")
                f.write(f"GroupSize,{args.groupsize}\n")
                f.write(f"Cost,{args.cost}\n")
                f.write(f"PartnerChoice,{args.p}\n")
                f.write(f"Reciprocity,{reciprocity}\n")
                f.write(f"IndirectR,{args.i}\n")
                f.write(f"Language,{args.language}\n")
                f.write(f"Shuffle,{args.shuffle}\n")
                f.write(f"alpha,{alpha:.6}\n")
                f.write(f"logES,{loges}\n")
                f.write(f"Given,{args.given}\n")
            counter = counter + 1


if __name__ == "__main__":
    parsed_args = parse_args("Create input files for simulations")
    main(parsed_args)
