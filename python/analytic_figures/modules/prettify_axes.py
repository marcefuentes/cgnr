""" Prettify axes. """

import modules.settings as ss


def add_imshow_letters(kwargs):
    """Add letters to (nrows x ncols) matrix of axes."""

    nrows, ncols = kwargs["axs"].shape

    n = 0
    letter_position = 1.0 + ss.LETTER_POSITION
    for i in range(nrows):
        for j in range(ncols):
            n = i * ncols + j
            letter = chr(ord("a") + n % 26)
            if n >= 26:
                letter = letter + letter
            kwargs["axs"][i, j].text(
                0,
                letter_position,
                letter,
                transform=kwargs["axs"][i, j].transAxes,
                fontsize=ss.LETTER_LABEL_SIZE,
                weight="bold",
            )


def add_imshow_ticks(kwargs):
    """Set ticks for (nrows x ncols) matrix of axes."""

    nrows, ncols = kwargs["axs"].shape
    nr = len(kwargs["y_values"])
    nc = len(kwargs["x_values"])
    xmin = min(kwargs["x_values"])
    xmax = max(kwargs["x_values"])
    ymin = min(kwargs["y_values"])
    ymax = max(kwargs["y_values"])

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
            )
    for ax in kwargs["axs"][:, 0]:
        ax.set_yticklabels([f"{ymax:.1f}", f"{(ymin + ymax)/2.:.1f}", f"{ymin:.1f}"])
    for ax in kwargs["axs"][-1, :]:
        ax.set_xticklabels([f"{xmin:.0f}", f"{(xmin + xmax)/2.:.0f}", f"{xmax:.0f}"])


def add_imshow_titles(kwargs):
    """Add titles to (nrows x ncols) matrix of axes."""

    for ax, title in zip(kwargs["axs"][0, :], kwargs["column_titles"]):
        ax.set_title(
            title, pad=ss.PLOT_SIZE * ss.TITLE_PADDING, fontsize=ss.LETTER_LABEL_SIZE
        )
    if kwargs["row_titles"]:
        for ax, title in zip(kwargs["axs"][:, -1], kwargs["row_titles"]):
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


def add_plot_letters(kwargs):
    """Add letters to (nrows x ncols x nr x nc) matrix of axes."""

    nrows, ncols, nr, _ = kwargs["axs"].shape

    letter_position = 1.0 + ss.LETTER_POSITION * nr

    for i in range(nrows):
        for j in range(ncols):
            n = i * ncols + j
            letter = chr(ord("a") + n % 26)
            if n >= 26:
                letter = letter + letter
            kwargs["axs"][i, j, 0, 0].text(
                0,
                letter_position,
                letter,
                fontsize=ss.LETTER_LABEL_SIZE,
                transform=kwargs["axs"][i, j, 0, 0].transAxes,
                weight="bold",
            )


def add_plot_ticks(kwargs):
    """Set ticks for (nrows x ncols x nr x nc) matrix of axes."""

    axs = kwargs["axs"]
    nrows, ncols, nr, nc = axs.shape
    step = int(nr / 2)
    y_min, y_max = axs[0, 0, 0, 0].get_ylim()
    y_middle = (y_min + y_max) / 2
    x_min, x_max = axs[0, 0, 0, 0].get_xlim()
    x_middle = (x_min + x_max) / 2

    for i in range(nrows):
        for j in range(ncols):
            for k in range(0, nr, step):
                axs[i, j, k, 0].set(yticks=[y_middle], yticklabels=[])
                axs[i, j, k, 0].tick_params(axis="y", labelsize=ss.TICK_LABEL_SIZE, size=ss.TICK_SIZE)
            for m in range(0, nc, step):
                axs[i, j, -1, m].set(xticks=[x_middle], xticklabels=[])
                axs[i, j, -1, m].tick_params(axis="x", labelsize=ss.TICK_LABEL_SIZE, size=ss.TICK_SIZE)
    for i in range(nrows):
        for k in range(0, nc, step):
            axs[i, 0, k, 0].set_yticklabels([kwargs["y_values"][k]])
    for j in range(ncols):
        for m in range(0, nr, step):
            axs[-1, j, -1, m].set_xticklabels([f"{kwargs['x_values'][m]:.0f}"])

def add_plot_titles(kwargs):
    """Add titles to (nrows x ncols x nr x nc) matrix of axes."""

    nrows, ncols, nr, nc = kwargs["axs"].shape

    for j in range(ncols):
        kwargs["axs"][0, j, 0, int(nc / 2)].set_title(
            kwargs["column_titles"][j],
            pad=ss.PLOT_SIZE * ss.TITLE_PADDING,
            fontsize=ss.LETTER_LABEL_SIZE,
        )
    for i in range(nrows):
        kwargs["axs"][i, -1, int(nr / 2), -1].annotate(
            kwargs["row_titles"][i],
            xy=(1, 0.5),
            xycoords="axes fraction",
            xytext=(ss.PLOT_SIZE * ss.TITLE_PADDING, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            fontsize=ss.LETTER_LABEL_SIZE,
        )


def prettify_imshow_axes(kwargs):
    """Prettify (nrows x ncols) matrix of axes."""

    nrows, ncols = kwargs["axs"].shape

    add_imshow_ticks(kwargs)
    add_imshow_titles(kwargs)
    add_imshow_letters(kwargs)

    for i in range(nrows):
        for j in range(ncols):
            kwargs["axs"][nrows - i - 1, j].set_axes_locator(
                kwargs["divider"].new_locator(nx=2 * j, ny=2 * i)
            )

    for i in range(nrows):
        for j in range(ncols):
            for spine in kwargs["axs"][i, j].spines.values():
                spine.set_linewidth(ss.LINE_WIDTH)


def prettify_plot_axes(kwargs):
    """Prettify (nrows x ncols x nr x nc) matrix of axes."""

    nrows, ncols, nr, nc = kwargs["axs"].shape

    for i in range(nrows):
        for j in range(ncols):
            for k in range(nr):
                for m in range(nc):
                    set_plot_spines(kwargs["axs"][i, j, k, m])
                    remove_ticks(kwargs["axs"][i, j, k, m])
                    set_plot_limits(kwargs["axs"][i, j, k, m])
                    set_plot_locator(
                        kwargs["axs"][i, j, k, m],
                        kwargs["divider"],
                        j * (nc + 1) + m + int(m / nc),
                        (nrows - i - 1) * (nr + 1) + nr - k - int(k / nr) - 1
                    )

    add_plot_titles(kwargs)
    add_plot_letters(kwargs)
    add_plot_ticks(kwargs)


def remove_ticks(ax):
    """Remove ticks for axes."""

    ax.set(xticks=[], yticks=[])


def set_plot_limits(ax):
    """Set limits for x and y axes for (nrows x ncols x nr x nc) matrix of axes."""

    ax.set(xlim=[-2, ss.N_X_VALUES + 1], ylim=[0, 0.25])


def set_plot_locator(ax, divider, nx, ny):
    """Set locator for axes."""

    ax.set_axes_locator(divider.new_locator(nx=nx, ny=ny))


def set_plot_spines(ax):
    """Set spines for axes."""

    for spine in ax.spines.values():
        spine.set_linewidth(ss.LINE_WIDTH)
