""" Add letters. """


def add_letters(axs, position, params):
    """Add letters."""

    nrows, ncols = axs.shape[:2]

    for i in range(nrows):
        for j in range(ncols):
            n = i * ncols + j
            params["s"] = chr(ord("a") + n % 26)
            params["transform"] = axs[i, j, 0, 0].transAxes
            if n >= 26:
                params["s"] = params["s"] + params["s"]
            axs[i, j, 0, 0].text(*position, **params)
