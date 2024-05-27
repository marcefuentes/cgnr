""" Save the figure to a file. """

from modules.save_image import save_image
from modules.save_movie import save_movie


def save_file(fig, data_dict):
    """Save the figure to a file."""

    if data_dict["movie"]:
        save_movie(fig, data_dict)
    else:
        save_image(data_dict)
