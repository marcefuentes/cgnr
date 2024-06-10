""" Save the figure to a file. """

from modules.save_image import save_image
from modules.save_movie import save_movie


def save_file(fig, update_args, options, data):
    """Save the figure to a file."""

    if options["movie"]:
        save_movie(fig, update_args, options, data)
    else:
        save_image(update_args, options, data)
