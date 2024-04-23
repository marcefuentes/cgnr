""" Prettify axes. """

import modules.settings as ss


def add_letters(ax, letter_position, n):
    """Add letters."""

    letter = chr(ord("a") + n % 26)
    if n >= 26:
        letter = letter + letter
    ax.text(
        0,
        letter_position,
        letter,
        fontsize=ss.LETTER_LABEL_SIZE,
        transform=ax.transAxes,
        weight="bold",
    )


def add_ticklabels_imshow(kwargs):
    """Add tick labels for (nrows x ncols)."""

    xmin = min(kwargs["x_values"])
    xmax = max(kwargs["x_values"])
    ymin = min(kwargs["y_values"])
    ymax = max(kwargs["y_values"])

    for ax in kwargs["axs"][:, 0]:
        ax.set_yticklabels([f"{ymax:.1f}", f"{(ymin + ymax)/2.:.1f}", f"{ymin:.1f}"])
    for ax in kwargs["axs"][-1, :]:
        ax.set_xticklabels([f"{xmin:.0f}", f"{(xmin + xmax)/2.:.0f}", f"{xmax:.0f}"])


def add_ticklabels_plot(kwargs):
    """Add tick labels for (nrows x ncols x nr x nc)."""

    nrows, ncols, nr, nc = kwargs["axs"].shape

    for i in range(nrows):
        for k in range(0, nr, nr // 2):
            kwargs["axs"][i, 0, k, 0].set_yticklabels([f"{kwargs['y_values'][k]:.1f}"])
    for j in range(ncols):
        for m in range(0, nc, nc // 2):
            kwargs["axs"][-1, j, -1, m].set_xticklabels(
                [f"{kwargs['x_values'][m]:.0f}"]
            )


def add_ticks_imshow(kwargs):
    """Set ticks for (nrows x ncols) matrix."""

    nrows, ncols = kwargs["axs"].shape
    nr = len(kwargs["y_values"])
    nc = len(kwargs["x_values"])

    for i in range(nrows):
        for j in range(ncols):
            kwargs["axs"][i, j].set(
                xticks=[0, 0.5 * (nc - 1), nc - 1],
                yticks=[0, 0.5 * (nr - 1), nr - 1],
                xticklabels=[],
                yticklabels=[],
            )
            kwargs["axs"][i, j].tick_params(
                axis="both",
                labelsize=ss.TICK_LABEL_SIZE,
                size=ss.TICK_SIZE,
                color=ss.TICK_COLOR,
            )


def add_ticks_plot(kwargs):
    """Set ticks for (nrows x ncols x nr x nc)."""

    axs = kwargs["axs"]
    nrows, ncols, nr, nc = axs.shape
    y_min, y_max = axs[0, 0, 0, 0].get_ylim()
    x_min, x_max = axs[0, 0, 0, 0].get_xlim()

    for i in range(nrows):
        for j in range(ncols):
            for k in range(0, nr, nr // 2):
                axs[i, j, k, 0].set(yticks=[(y_min + y_max) / 2], yticklabels=[])
                axs[i, j, k, 0].tick_params(
                    axis="y",
                    labelsize=ss.TICK_LABEL_SIZE,
                    size=ss.TICK_SIZE,
                    color=ss.TICK_COLOR,
                )
            for m in range(0, nc, nc // 2):
                axs[i, j, -1, m].set(xticks=[(x_min + x_max) / 2], xticklabels=[])
                axs[i, j, -1, m].tick_params(
                    axis="x",
                    labelsize=ss.TICK_LABEL_SIZE,
                    size=ss.TICK_SIZE,
                    color=ss.TICK_COLOR,
                )


def add_title_column(ax, title):
    """Add title."""

    ax.set_title(
        title,
        pad=ss.PLOT_SIZE * ss.TITLE_PADDING,
        fontsize=ss.LETTER_LABEL_SIZE,
    )


def add_title_row(ax, title):
    """Add title."""

    ax.annotate(
        title,
        xy=(1, 0.5),
        xycoords="axes fraction",
        xytext=(ss.PLOT_SIZE * ss.TITLE_PADDING, 0),
        textcoords="offset points",
        va="center",
        ha="left",
        fontsize=ss.LETTER_LABEL_SIZE,
    )


def prettify_axes_imshow(kwargs):
    """Prettify (nrows x ncols) matrix."""

    nrows, ncols = kwargs["axs"].shape
    letter_position = 1.0 + ss.LETTER_POSITION

    add_ticks_imshow(kwargs)
    add_ticklabels_imshow(kwargs)

    for i in range(nrows):
        for j in range(ncols):
            add_letters(kwargs["axs"][i, j], letter_position, i * ncols + j)
            set_spines(kwargs["axs"][i, j])
            set_locator(
                kwargs["axs"][nrows - i - 1, j], kwargs["divider"], 2 * j, 2 * i
            )
    for j, title in enumerate(kwargs["column_titles"]):
        add_title_column(kwargs["axs"][0, j], title)
    for i, title in enumerate(kwargs["row_titles"]):
        add_title_row(kwargs["axs"][i, -1], title)


def prettify_axes_plot(kwargs):
    """Prettify (nrows x ncols x nr x nc) matrix."""

    nrows, ncols, nr, nc = kwargs["axs"].shape
    letter_position = 1.0 + ss.LETTER_POSITION * nr

    for i in range(nrows):
        for j in range(ncols):
            add_letters(kwargs["axs"][i, j, 0, 0], letter_position, i * ncols + j)
            for k in range(nr):
                for m in range(nc):
                    set_spines(kwargs["axs"][i, j, k, m])
                    set_locator(
                        kwargs["axs"][i, j, k, m],
                        kwargs["divider"],
                        j * (nc + 1) + m + int(m / nc),
                        (nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1,
                    )
                    remove_ticks(kwargs["axs"][i, j, k, m])
                    set_plot_limits(
                        kwargs["axs"][i, j, k, m], kwargs["x_lim"], kwargs["y_lim"]
                    )

    for j, title in enumerate(kwargs["column_titles"]):
        add_title_column(kwargs["axs"][0, j, 0, int(nc / 2)], title)
    for i, title in enumerate(kwargs["row_titles"]):
        add_title_row(kwargs["axs"][i, -1, int(nr / 2), -1], title)
    add_ticks_plot(kwargs)
    add_ticklabels_plot(kwargs)


def remove_ticks(ax):
    """Remove ticks."""

    ax.set(xticks=[], yticks=[])


def set_locator(ax, divider, nx, ny):
    """Set locator."""

    ax.set_axes_locator(divider.new_locator(nx=nx, ny=ny))


def set_plot_limits(ax, xlim, ylim):
    """Set limits."""

    ax.set(xlim=xlim, ylim=ylim)


def set_spines(ax):
    """Set spines."""

    for spine in ax.spines.values():
        spine.set_linewidth(ss.BORDER_WIDTH)
