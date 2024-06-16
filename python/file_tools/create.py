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

    constant_lines = [
        f"Seed,1\n",
        f"N,{project['N']}\n",
        f"Runs,{project['Runs']}\n",
        f"Time,{project['Time']}\n",
        f"Periods,{project['Periods']}\n",
        f"qBMutationSize,{project['qBMutationSize']}\n",
        f"GrainMutationSize,{project['GrainMutationSize']}\n",
        f"DeathRate,{project['DeathRate']}\n",
    ]

    reciprocity = 1 if args.d or args.i else 0
    option_lines = [
        f"GroupSize,{args.groupsize}\n",
        f"Cost,{args.cost}\n",
        f"PartnerChoice,{args.p}\n",
        f"Reciprocity,{reciprocity}\n",
        f"IndirectR,{args.i}\n",
        f"Language,{args.language}\n",
        f"Shuffle,{args.shuffle}\n",
    ]

    alphas = np.linspace(project["alpha_min"], project["alpha_max"], project["grid"])
    logess = np.linspace(project["loges_min"], project["loges_max"], project["grid"])

    for alpha in alphas:
        for loges in logess:
            filename = f"{path}/{counter}{input_file_extension}"
            print(f"\r{filename}", end="", flush=True)
            with open(filename, "w", encoding="utf-8") as f:
                remaining_lines = [
                    f"alpha,{alpha:.6}\n",
                    f"logES,{loges}\n",
                    f"Given,{args.given}\n",
                ]
                f.writelines(constant_lines)
                f.writelines(option_lines)
                f.writelines(remaining_lines)
            counter = counter + 1
    print()


if __name__ == "__main__":
    parsed_args = parse_args("Create input files for simulations")
    main(parsed_args)
