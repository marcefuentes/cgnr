""" Parses the arguments of the command line. """

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from importlib import import_module


def parse_args():
    """Parse command line arguments and return them as a dictionary"""

    description = "description: Plot"

    parser = ArgumentParser(
        description=description, formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--results", action="store_true", help="Use results module")
    parser.add_argument("--icurves", action="store_true", help="Use icurves module")

    preliminary_args, remaining_args = parser.parse_known_args()

    if preliminary_args.results and preliminary_args.icurves:
        parser.error("Specify only one of --results or --icurves")

    if preliminary_args.results:
        module_name = "resultsm"
    elif preliminary_args.icurves:
        module_name = "icurvesm"
    else:
        module_name = None
        parser.error("Must specify either --results or --icurves")

    # Dynamically import the appropriate parse_args function
    parse_args_module = import_module(f"{module_name}.parse_args")
    data, image = parse_args_module.parse_args(remaining_args)

    return data, image
