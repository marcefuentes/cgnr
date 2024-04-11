
""" Reads the config file and returns the value of the variable passed as argument """

import configparser
import os

import common_modules.colors as cc

def get_config(variable):
    """ Reads the config file and returns the value of the variable passed as argument """

    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config.ini")
    if not config_file_path:
        return RuntimeError("config.ini does not exist in the root of the project")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    if config.has_option('DEFAULT', variable):
        if variable in ("hours", "number_of_lines"):
            return config.getint('DEFAULT', variable)
        if variable in ("alpha_min", "alpha_max", "loges_min", "loges_max"):
            return config.getfloat('DEFAULT', variable)
        if variable in ("output_file_extensions", "constraints"):
            return config.get("DEFAULT", variable).split(",")
        return config.get('DEFAULT', variable)
    print(f"{color.BOLD}{color.RED}{variable} not found in {config_file_path}{color.RESET}")
    return 0
