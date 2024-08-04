""" Parses the arguments of the command line. """

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from inspect import isfunction

from icurvess import layouts


def parse_args():
    """Parse command line arguments and return them as a dictionary"""

    description = (
        "Plot indifference curves and budget constraints, and fitness landscapes."
    )

    parser = ArgumentParser(
        description=description, formatter_class=ArgumentDefaultsHelpFormatter
    )

    layout_names = [
        name for name in layouts.__all__ if isfunction(getattr(layouts, name))
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
