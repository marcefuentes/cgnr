""" Reads the config file and returns the value of the variable passed as argument """

import configparser
import os

from common_modules import color

VARIABLE_TYPES = {
    "Cost": "int",
    "DeathRate": "int",
    "Given": "float",
    "GrainMutationSize": "int",
    "GroupSize": "int",
    "N": "int",
    "Periods": "int",
    "Runs": "int",
    "alpha_max": "float",
    "alpha_min": "float",
    "bins": "int",
    "constraints": "list",
    "grid": "int",
    "hours": "int",
    "loges_max": "float",
    "loges_min": "float",
    "number_of_lines": "int",
    "output_file_extensions": "list",
    "qBMutationSize": "int",
}


def get_config(variable):
    """Reads the config file and returns the value of the variable passed as argument"""

    config_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../config.ini"
    )
    if not os.path.exists(config_file_path):
        return RuntimeError("config.ini does not exist in the root of the project")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    if not config.has_option("DEFAULT", variable):
        print(
            f"{color.BOLD}{color.RED}Variable {variable} not found in config.ini{color.RESET}"
        )
        return 0

    variable_type = VARIABLE_TYPES.get(variable, "float")

    if variable_type == "float":
        return config.getfloat("DEFAULT", variable)
    if variable_type == "int":
        return config.getint("DEFAULT", variable)
    if variable_type == "list":
        return config.get("DEFAULT", variable).split(",")
    return config.get("DEFAULT", variable)
