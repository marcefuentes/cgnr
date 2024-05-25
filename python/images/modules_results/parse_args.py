""" Parses the arguments of the command line. """

import argparse
import os

import modules_results.layouts_single_folder as s_folder
from modules_results.trait_map import trait_map


def parse_args():
    """Parse command line arguments and return them."""

    folder = os.path.basename(os.getcwd())

    if folder.startswith("0") or folder.startswith("1"):
        single_trait = True
        single_folder = True
        description = "description: Plot results for a trait in this folder"
        choices_trait_set = list(trait_map.keys())
        arg_help = "trait (required)"
    elif folder == "results":
        single_trait = True
        single_folder = False
        description = "description: Plot results for a trait across several variants"
        choices_trait_set = list(trait_map.keys())
        arg_help = "trait (required)"
    else:
        single_trait = False
        single_folder = False
        description = "description: Plot results for several traits in this variant"
        choices_trait_set = list(s_folder.columns.keys())
        arg_help = "trait set (required)"

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    args_dict = {
        "trait_set": {
            "type": str,
            "choices": choices_trait_set,
            "help": arg_help,
        },
        "fitness": {"action": "store_true", "help": "add fitness curve"},
        "histogram": {"action": "store_true", "help": "add histogram"},
        "movie": {"action": "store_true", "help": "enable movie"},
        "clean": {"action": "store_true", "help": "clean folders"},
    }

    for arg, params in args_dict.items():
        parser.add_argument(f"--{arg}", **params)

    args = parser.parse_args()
    args.single_trait = single_trait
    args.single_folder = single_folder

    return args
