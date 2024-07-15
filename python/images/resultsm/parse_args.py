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

    layout_names = [
        name for name in layouts.__all__ if inspect.isfunction(getattr(layouts, name))
    ]

    args_dict = {
        "givens": {
            "type": str,
            "choices": ["0.0", "0.5", "1.0"],
            "default": "1.0",
            "help": "given folder",
        },
        "givens_control": {
            "type": str,
            "choices": ["none", "0.0", "0.5", "1.0"],
            "default": "none",
            "help": "given folder (control)",
        },
        "layout": {
            "type": str,
            "choices": layout_names,
            "default": "theory",
            "help": "figure",
        },
        "mechanisms": {
            "type": str,
            "choices": ["none", "d", "i", "p", "pd", "pi"],
            "default": "none",
            "help": "mechanism",
        },
        "mechanisms_control": {
            "type": str,
            "choices": ["none", "d", "i", "p", "pd", "pi"],
            "default": "none",
            "help": "mechanism (control)",
        },
        "traits": {
            "type": str,
            "help": "trait",
        },
        "traits_control": {
            "type": str,
            "default": "none",
            "help": "trait (control)",
        },
        "histogram": {"action": "store_true", "help": "add histogram"},
        "lang": {"action": "store_true", "help": "lang folders"},
        "movie": {"action": "store_true", "help": "enable movie"},
        "clean": {"action": "store_true", "help": "clean folders"},
    }

    for arg, params in args_dict.items():
        parser.add_argument(f"--{arg}", **params)

    args = parser.parse_args()

    if args.traits_control == "none":
        args.traits_control = args.traits

    if args.givens_control == "none":
        args.givens_control = args.given

    if args.layout == "curves":
        args.ax_type = "PolyCollection"
    elif args.histogram:
        args.ax_type = "Line2D"
    else:
        args.ax_type = "AxesImage"

    return args
