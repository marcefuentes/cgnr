""" Parses the arguments of the command line. """

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from inspect import isfunction

from modules.add_layout import add_layout
from resultss import layouts
from resultss.image import image


def parse_args(args):
    """Parse command line arguments and return them as a dictionary"""

    description = "description: Plot results"

    parser = ArgumentParser(
        description=description, formatter_class=ArgumentDefaultsHelpFormatter
    )

    layout_names = [
        name for name in layouts.__all__ if isfunction(getattr(layouts, name))
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
        "lang": {
            "type": str,
            "choices": ["lang", "nolang"],
            "default": "nolang",
            "help": "language",
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
        "clean": {"action": "store_true", "help": "clean folders"},
        "histogram": {"action": "store_true", "help": "add histogram"},
        "movie": {"action": "store_true", "help": "enable movie"},
    }

    for arg, params in args_dict.items():
        parser.add_argument(f"--{arg}", **params)

    args = parser.parse_args(args)

    if args.traits_control == "none":
        args.traits_control = args.traits

    if args.givens_control == "none":
        args.givens_control = args.givens

    data = vars(args)
    if data["layout"] == "curves":
        data["ax_type"] = "PolyCollection"
    elif data["histogram"]:
        data["ax_type"] = "Line2D"
    else:
        data["ax_type"] = "AxesImage"

    data["module_folder"] = "resultsm"
    add_layout(data, layouts)

    return data, image
