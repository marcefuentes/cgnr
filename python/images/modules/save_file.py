""" Save the figure to a file. """

from matplotlib.pyplot import close
from modules.save_image import save_image
from modules.save_movie import save_movie


def save_file(fig, data):
    """Save the figure to a file."""

    if data["movie"]:
        save_movie(fig, data)
    else:
        save_image(data)

    close(fig)
