""" Reads the config file and returns the value of the variable passed as argument """

import configparser
import os

from common_modules import color


def get_config(variable):
    """Reads the config file and returns the value of the variable passed as argument"""

    config_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../config.ini"
    )
    if not config_file_path:
        return RuntimeError("config.ini does not exist in the root of the project")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    float_variables = ["Given", "alpha_max", "alpha_min", "loges_max", "loges_min"]
    int_variables = [
        "Cost",
        "DeathRate",
        "GrainMutationSize",
        "GroupSize",
        "N",
        "Periods",
        "Runs",
        "bins",
        "grid",
        "hours",
        "number_of_lines",
        "qBMutationSize",
    ]
    list_variables = ["constraints", "output_file_extensions"]

    if config.has_option("DEFAULT", variable):
        if variable in float_variables:
            return config.getfloat("DEFAULT", variable)
        if variable in int_variables:
            return config.getint("DEFAULT", variable)
        if variable in list_variables:
            return config.get("DEFAULT", variable).split(",")
        return config.get("DEFAULT", variable)
    print(
        f"{color.BOLD}{color.RED}{variable} not found in {config_file_path}{color.RESET}"
    )
    return 0
