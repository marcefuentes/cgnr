""" Add letters. """


def add_letters(ax_type, axs, params):
    """Add letters."""

    if ax_type == "Line2D" or ax_type == "PolyCollection":
        add_letters_line2d(axs, params)
    else:
        add_letters_axesimage(axs, params)


def add_letters_axesimage(axs, params):
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
        ax.text(**params)
        i += 1


def add_letters_line2d(axs, params):
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
            axs[i, j, 0, 0].text(**params)
