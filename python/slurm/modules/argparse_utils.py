
""" Parses the arguments of the command line. """

import argparse

def parse_args(description):
    """Parse arguments"""

    parser = argparse.ArgumentParser(
        description=f"description: {description}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    if "Inventory" in description:
        parser.add_argument(
            "--store",
            action="store_true",
            help="Inventory 'Store' filesystem in cesga"
        )
    if "Submit" in description or "Resubmit" in description:
        parser.add_argument(
            "--test",
            action="store_true",
            help="Run test in cesga"
        )
    args = parser.parse_args()

    return args
