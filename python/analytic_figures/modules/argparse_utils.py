
""" Parses the arguments of the command line. """

import argparse

def parse_args(description, trait_choices):
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(
        description=f"description: {description}", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "mode",
        choices=trait_choices,
        help="Mode (required)"
    )
    parser.add_argument(
        "--histogram",
        action="store_true",
        help="Add histogram"
    )
    parser.add_argument(
        "--movie",
        action="store_true",
        help="Enable movie"
    )

    args = parser.parse_args()

    if args.mode not in trait_choices:
        parser.error(f"Invalid mode: {args.mode}")

    return args
