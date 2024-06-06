""" Parses the arguments of the command line. """

import argparse
import os

from settings_results.trait_map import trait_map


def parse_args():
    """Parse command line arguments and return them as a dictionary"""

    description = "description: Plot results"

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    args_dict = {
        "trait_set": {
            "type": str,
            "choices": list(trait_map.keys()),
            "help": "trait (required)",
        },
        "figure": {
            "type": str,
            "choices": ["figure_2", "figure_3", "p_fitness"],
            "default": "figure_3",
            "help": "figure",
        },
        "given": {
            "type": str,
            "choices": ["0.5", "1.0"],
            "default": "1.0",
            "help": "given folder",
        },
        "mechanism": {
            "type": str,
            "choices": ["none", "d", "i", "p", "pd", "pi"],
            "default": "none",
            "help": "mechanism",
        },
        "fitness": {"action": "store_true", "help": "add fitness curve"},
        "histogram": {"action": "store_true", "help": "add histogram"},
        "movie": {"action": "store_true", "help": "enable movie"},
        "clean": {"action": "store_true", "help": "clean folders"},
    }

    for arg, params in args_dict.items():
        parser.add_argument(f"--{arg}", **params)

    args = parser.parse_args()

    if args.figure == "figure_2":
        args.trait_set = "w"

    return args
