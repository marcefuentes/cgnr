""" Format artists. """

import numpy as np


def artists_format(artists, params):
    """Format artists."""

    for idx in np.ndindex(artists.shape):
        artists[idx].set(**params)
