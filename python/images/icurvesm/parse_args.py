""" Parses the arguments of the command line. """

import argparse
import inspect

from icurvess import layouts


def parse_args():
    """Parse command line arguments and return them as a dictionary"""

    description = (
        "Plot indifference curves and budget constraints, and fitness landscapes."
    )

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    layout_names = [
        name for name in layouts.__all__ if inspect.isfunction(getattr(layouts, name))
    ]

    args_dict = {
        "layout": {
            "type": str,
            "choices": layout_names,
            "default": "m01",
            "help": "figure",
        },
        "movie": {"action": "store_true", "help": "enable movie"},
    }

    for arg, params in args_dict.items():
        parser.add_argument(f"--{arg}", **params)

    args = parser.parse_args()

    return args
