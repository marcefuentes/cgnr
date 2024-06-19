""" Parses the arguments of the command line. """

import argparse
import inspect

from resultss import layouts


def parse_args():
    """Parse command line arguments and return them as a dictionary"""

    description = "description: Plot results"

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    layout_names = [name for name, _ in inspect.getmembers(layouts, inspect.isfunction)]

    args_dict = {
        "given": {
            "type": str,
            "choices": ["0.0", "0.5", "1.0"],
            "default": "1.0",
            "help": "given folder",
        },
        "layout": {
            "type": str,
            "choices": layout_names,
            "default": "default",
            "help": "figure",
        },
        "mechanism": {
            "type": str,
            "choices": ["none", "d", "i", "p", "pd", "pi", "social"],
            "default": "none",
            "help": "mechanism",
        },
        "mechanism_control": {
            "type": str,
            "choices": ["none", "d", "i", "p", "pd", "pi", "social"],
            "default": "none",
            "help": "mechanism",
        },
        "trait": {
            "type": str,
            "help": "trait (required)",
        },
        "trait_control": {
            "type": str,
            "default": "none",
            "help": "trait (control)",
        },
        "histogram": {"action": "store_true", "help": "add histogram"},
        "movie": {"action": "store_true", "help": "enable movie"},
        "clean": {"action": "store_true", "help": "clean folders"},
    }

    for arg, params in args_dict.items():
        parser.add_argument(f"--{arg}", **params)

    args = parser.parse_args()

    if args.trait_control == "none":
        args.trait_control = args.trait

    return args
