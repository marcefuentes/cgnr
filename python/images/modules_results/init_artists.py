""" Initialize artists for plotting. """

import numpy as np

from common_modules.get_config import get_config
from modules.get_setting import get_setting as get


def init_imshow_artists(axs, _, kwargs):
    """Initialize (nrows x ncols) matrix of AxesImage artists."""

    nrows, ncols = axs.shape
    kwargs["artists"] = np.empty_like(axs)
    dummy_zmatrix = np.zeros((kwargs["nr"], kwargs["nc"]))

    for r in range(nrows):
        for c in range(ncols):
            kwargs["artists"][r, c] = axs[r, c].imshow(
                dummy_zmatrix, cmap=get("COMMON", "color_map"), vmin=-1, vmax=1
            )
    return kwargs


def init_plot_artists(axs, file_name, kwargs):
    """Initialize(nrows x ncols x nr x nc) matrix of Line2D artists."""

    nrows, ncols, _, _ = axs.shape
    kwargs["artists"] = np.empty_like(axs)
    x = np.arange(get_config("bins"))
    dummy_y = np.zeros_like(x)

    for r in range(nrows):
        for c in range(ncols):
            for a in range(kwargs["nr"]):
                for e in range(kwargs["nc"]):
                    (kwargs["artists"][r, c, a, e],) = axs[r, c, a, e].plot(
                        x, dummy_y, c="black", lw=get("COMMON", "line_width")
                    )
    return kwargs
