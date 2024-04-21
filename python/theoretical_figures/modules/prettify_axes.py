""" Prettify axes. """

import modules.settings as ss


def add_plot_letters(kwargs):
    """Add letters to (nrows x ncols x nr x nc) matrix of axes."""

    nrows, ncols, nr, _ = kwargs["axs"].shape

    letter_position = 1.0 + ss.LETTER_POSITION * nr

    for r in range(nrows):
        for c in range(ncols):
            i = r * ncols + c
            letter = chr(ord("a") + i % 26)
            if i >= 26:
                letter = letter + letter
            kwargs["axs"][r, c, 0, 0].text(
                0,
                letter_position,
                letter,
                fontsize=ss.LETTER_LABEL_SIZE,
                transform=kwargs["axs"][r, c, 0, 0].transAxes,
                weight="bold",
            )


def add_plot_ticks(kwargs):
    """Set ticks for (nrows x ncols x nr x nc) matrix of axes."""

    axs = kwargs["axs"]
    x_values = kwargs["x_values"]
    y_values = kwargs["y_values"]
    nrows, ncols, nr, nc = axs.shape

    xlim = [0, 1]
    ylim = [0, 1]
    step = int(nr / 2)

    for r in range(nrows):
        for c in range(ncols):
            for a in range(nr):
                for e in range(nc):
                    axs[r, c, a, e].set(xticks=[], yticks=[], xlim=xlim, ylim=ylim)
                    axs[r, c, a, e].tick_params(
                        axis="both", labelsize=ss.TICK_LABEL_SIZE, size=ss.TICK_SIZE
                    )
            for a in range(0, nr, step):
                axs[r, c, a, 0].set(yticks=[ylim[1] / 2], yticklabels=[])
            for e in range(0, nc, step):
                axs[r, c, -1, e].set(xticks=[xlim[1] / 2], xticklabels=[])
        for a in range(0, nr, step):
            axs[r, 0, a, 0].set_yticklabels([y_values[a]])

    for c in range(ncols):
        for e in range(0, nc, step):
            axs[-1, c, -1, e].set_xticklabels([f"{x_values[e]:.0f}"])


def prettify_plot_axes(kwargs):
    """Prettify (nrows x ncols x nr x nc) matrix of axes."""

    nrows, ncols, nr, nc = kwargs["axs"].shape

    add_plot_ticks(kwargs)
    add_plot_letters(kwargs)

    for r in range(nrows):
        for c in range(ncols):
            for a in range(nr):
                inner_y = (nrows - r - 1) * (nr + 1) + nr - a - int(a / nr) - 1
                for e in range(nc):
                    inner_x = c * (nc + 1) + e + int(e / nc)
                    new_locator = kwargs["divider"].new_locator(nx=inner_x, ny=inner_y)
                    kwargs["axs"][r, c, a, e].set_axes_locator(new_locator)

    for r in range(nrows):
        for c in range(ncols):
            for a in range(nr):
                for e in range(nc):
                    for spine in kwargs["axs"][r, c, a, e].spines.values():
                        spine.set_linewidth(ss.LINE_WIDTH)
