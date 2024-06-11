""" Parses the arguments of the command line. """

import argparse


def parse_args(description, flag, flag_help):
    """Parse arguments"""

    parser = argparse.ArgumentParser(
        description=f"description: {description}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(flag, action="store_true", help=flag_help)

    args = parser.parse_args()
    return args
