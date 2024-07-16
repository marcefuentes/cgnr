""" Format artists. """

import numpy as np


def format_artists(artists, params):
    """Format artists."""

    for idx in np.ndindex(artists.shape):
        artists[idx].set(**params)
