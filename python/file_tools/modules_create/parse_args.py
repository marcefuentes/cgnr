""" Parses the arguments of the command line. """

import argparse

from common_modules.get_config import get_config


def parse_args(description):
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description=f"description: {description}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    default_groupsize = get_config("GroupSize")
    default_cost = get_config("Cost")
    default_given = get_config("Given")

    parser.add_argument(
        "--groupsize", type=int, default=default_groupsize, help="group size"
    )
    parser.add_argument("--cost", type=float, default=default_cost, help="cost value")
    parser.add_argument(
        "--partnerchoice",
        action="store_const",
        const=1,
        default=0,
        help="enable partnerchoice",
    )
    parser.add_argument(
        "--directr",
        action="store_const",
        const=1,
        default=0,
        help="enable direct reciprocity",
    )
    parser.add_argument(
        "--indirectr",
        action="store_const",
        const=1,
        default=0,
        help="enable indirect reciprocity",
    )
    parser.add_argument(
        "--language", action="store_const", const=1, default=0, help="enable language"
    )
    parser.add_argument(
        "--shuffle", action="store_const", const=1, default=0, help="enable shuffling"
    )
    parser.add_argument(
        "--given", type=float, default=default_given, help="given value"
    )

    args = parser.parse_args()
    return args
