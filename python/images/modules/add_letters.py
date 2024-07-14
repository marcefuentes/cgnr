""" Add letters. """


def add_letters(axs, position, params):
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
