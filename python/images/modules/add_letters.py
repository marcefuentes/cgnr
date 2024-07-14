""" Add letters. """


def add_letters(axs, position, params):
    """Add letters."""

    nrows, ncols = axs.shape[:2]

    for i in range(nrows):
        for j in range(ncols):
            n = i * ncols + j
            letter = chr(ord("a") + n % 26)
            if letter == "h":
                letter = "f"
            if letter == "i":
                letter = "g"
            if letter == "j":
                letter = "h"
            if n >= 26:
                letter += letter
            params["s"] = letter
            params["transform"] = axs[i, j, 0, 0].transAxes
            axs[i, j, 0, 0].text(*position, **params)
