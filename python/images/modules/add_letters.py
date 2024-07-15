""" Add letters. """


def add_letters_imshow(axs, position, params):
    """Add letters."""

    i = 0
    for ax in axs.flatten():
        if not ax.axes:
            continue

        letter = chr(ord("a") + i % 26)
        if i >= 26:
            letter += letter
        params["s"] = letter
        params["transform"] = ax.transAxes
        ax.text(*position, **params)
        i += 1


def add_letters_line2d(axs, position, params):
    """Add letters."""

    nrows, ncols = axs.shape[:2]

    for i in range(nrows):
        for j in range(ncols):
            n = i * ncols + j
            letter = chr(ord("a") + n % 26)
            if n >= 26:
                letter += letter
            params["s"] = letter
            params["transform"] = axs[i, j, 0, 0].transAxes
            axs[i, j, 0, 0].text(*position, **params)
