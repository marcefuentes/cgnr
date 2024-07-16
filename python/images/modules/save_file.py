""" Save the figure to a file. """

from modules.save_image import save_image
from modules.save_movie import save_movie


def save_file(fig, data, options):
    """Save the figure to a file."""

    if options["movie"]:
        save_movie(fig, data, options)
    else:
        save_image(data, options)
