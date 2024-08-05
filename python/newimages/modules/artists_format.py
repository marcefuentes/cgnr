""" Format artists. """

from numpy import ndindex


def artists_format(artists, params):
    """Format artists."""

    for idx in ndindex(artists.shape):
        artists[idx].set(**params)
