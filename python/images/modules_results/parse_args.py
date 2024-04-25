""" Parses the arguments of the command line. """

import argparse
import os

import modules_results.modes as mm


def parse_args():
    """Parse command line arguments."""

    if os.path.basename(os.getcwd()) == "results":
        mode_is_trait = True
        description = "description: Plot results for a trait"
        choices = list(mm.dict_traits.keys())
        arg_help = "trait (required)"
    else:
        mode_is_trait = False
        description = "description: Plot results in this folder"
        choices = list(mm.dict_multitrait_columns.keys())
        arg_help = "mode (required)"

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("mode", type=str, choices=choices, help=arg_help)

    parser.add_argument("--histogram", action="store_true", help="add histogram")
    parser.add_argument("--movie", action="store_true", help="enable movie")
    parser.add_argument("--clean", action="store_true", help="clean folders")

    args = parser.parse_args()
    if args.mode not in choices:
        parser.error(f"Invalid mode: {args.mode}")
    args.mode_is_trait = mode_is_trait

    return args
