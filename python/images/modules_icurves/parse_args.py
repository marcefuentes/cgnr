""" Parses the arguments of the command line. """

import argparse


def parse_args():
    """Parse command line arguments."""

    description = (
        "Plot indifference curves and budget constraints, and fitness landscapes."
    )

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--movie", action="store_true", help="enable movie")

    args = parser.parse_args()

    return args
