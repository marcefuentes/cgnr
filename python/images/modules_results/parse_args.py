""" Parses the arguments of the command line. """

import argparse
import os

import modules_results.trait_sets_config as mm


def parse_args():
    """Parse command line arguments."""

    folder = os.path.basename(os.getcwd())

    if folder.startswith("0") or folder.startswith("1"):
        single_trait = True
        single_folder = True
        description = "description: Plot results for a trait in this folder"
        choices_trait_set = list(mm.dict_traits.keys())
        arg_help = "trait (required)"
    elif folder == "results":
        single_trait = True
        single_folder = False
        description = "description: Plot results for a trait across several variants"
        choices_trait_set = list(mm.dict_traits.keys())
        arg_help = "trait (required)"
    else:
        single_trait = False
        single_folder = False
        description = "description: Plot results for several traits in this variant"
        choices_trait_set = list(mm.dict_single_folder_columns.keys())
        arg_help = "trait set (required)"

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--trait_set", type=str, choices=choices_trait_set, help=arg_help
    )

    parser.add_argument("--curve", action="store_true", help="add curve")
    parser.add_argument("--histogram", action="store_true", help="add histogram")
    parser.add_argument("--movie", action="store_true", help="enable movie")
    parser.add_argument("--clean", action="store_true", help="clean folders")

    args = parser.parse_args()

    if args.trait_set not in choices_trait_set:
        parser.error(f"Invalid trait_set: {args.trait_set}")

    args.single_trait = single_trait
    args.single_folder = single_folder

    return args
