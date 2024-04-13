
""" Parses the arguments of the command line. """

import argparse
import os

import modules.modes as mm

def parse_args():
    """Parse command line arguments."""

    if os.path.basename(os.getcwd()) == "results":
        mode_is_trait = True
        choices = list(mm.dict_traits.keys())
        default = "w"
        arg_help = "trait (required)"
    else:
        mode_is_trait = False
        choices = list(mm.dict_columns.keys())
        default = "cooperation"
        arg_help = "mode (required)"

    parser = argparse.ArgumentParser(
        description=f"description: Plot results", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "mode",
        type=str,
        default=default,
        choices=choices,
        help=arg_help
    )

    parser.add_argument(
        "--histogram",
        action="store_true",
        help="add histogram"
    )
    parser.add_argument(
        "--movie",
        action="store_true",
        help="enable movie"
    )

    args = parser.parse_args()
    if args.mode not in choices:
        parser.error(f"Invalid mode: {args.mode}")

    return args, mode_is_trait
