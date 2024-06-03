""" Save the figure to a file. """

from modules.save_image import save_image
from modules.save_movie import save_movie


def save_file(fig, update_args, config_data, dynamic_data):
    """Save the figure to a file."""

    if config_data["movie"]:
        save_movie(fig, update_args, config_data, dynamic_data)
    else:
        save_image(update_args, config_data, dynamic_data)
