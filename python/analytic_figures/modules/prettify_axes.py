
""" Prettify axes. """

import modules.settings as ss

def prettify_imshow_axes(
    axs,
    divider,
    y_values,
    x_values,
    row_titles,
    column_titles
):
    """ Prettify (nrows x ncols) matrix of axes. """

    nrows, ncols = axs.shape
    nr = len(y_values)
    nc = len(x_values)

    xticks = [0, 0.5*(nc - 1), nc - 1]
    yticks = [0, 0.5*(nr - 1), nr - 1]
    xmin = min(x_values)
    xmax = max(x_values)
    ymin = min(y_values)
    ymax = max(y_values)
    xticklabels = [
        f"{xmin:.0f}",
        f"{(xmin + xmax)/2.:.0f}",
        f"{xmax:.0f}"
    ]
    yticklabels = [
        f"{ymax:.1f}",
        f"{(ymin + ymax)/2.:.1f}",
        f"{ymin:.1f}"
    ]

    for r in range(nrows):
        for c in range(ncols):
            axs[nrows - r - 1, c].set_axes_locator(
                divider.new_locator(nx=2*c, ny=2*r)
            )

    i = 0
    letter_position = 1.0 + ss.LETTER_POSITION
    for r in range(nrows):
        for c in range(ncols):
            ax = axs[r, c]
            i = r*ncols + c
            letter = chr(ord("a") + i % 26)
            if i >= 26:
                letter = letter + letter
            ax.text(
                0,
                letter_position,
                letter,
                transform=ax.transAxes,
                fontsize=ss.LETTER_LABEL_SIZE,
                weight="bold"
            )
            for spine in ax.spines.values():
                spine.set_linewidth(ss.LINE_WIDTH)
            ax.set(
                xticks=xticks,
                yticks=yticks,
                xticklabels=[],
                yticklabels=[]
            )
            ax.tick_params(
                axis="both",
                labelsize=ss.TICK_LABEL_SIZE,
                size=ss.TICK_SIZE,
            )
    for ax in axs[:, 0]:
        ax.set_yticklabels(yticklabels)
    for ax in axs[-1, :]:
        ax.set_xticklabels(xticklabels)
    for ax, title in zip(axs[0, :], column_titles):
        ax.set_title(
            title,
            pad=ss.PLOT_SIZE * ss.TITLE_PADDING,
            fontsize=ss.LETTER_LABEL_SIZE
        )
    if row_titles:
        for ax, title in zip(axs[:, -1], row_titles):
            ax.annotate(
                title,
                xy=(1, 0.5),
                xycoords="axes fraction",
                xytext=(ss.PLOT_SIZE * ss.TITLE_PADDING, 0),
                textcoords="offset points",
                va="center",
                ha="left",
                fontsize=ss.LETTER_LABEL_SIZE
            )

    return axs

def prettify_plot_axes(
    axs,
    divider,
    y_values,
    x_values,
    row_titles,
    column_titles
):
    """ Prettify (nrows x ncols x nr x nc) matrix of axes. """

    nrows, ncols, nr, nc = axs.shape

    xlim = [-2, ss.BINS + 1]
    ylim = [0, 0.25]
    step = int(nr/2)
    letter_position = 1.0 + ss.LETTER_POSITION * nr

    for r in range(nrows):
        for c in range(ncols):
            for a in range(nr):
                inner_y = (nrows - r - 1) * (nr + 1) + nr - a - int(a / nr) - 1
                for e in range(nc):
                    inner_x = c * (nc + 1) + e + int(e / nc)
                    new_locator = divider.new_locator(nx=inner_x, ny=inner_y)
                    ax = axs[r, c, a, e]
                    ax.set_axes_locator(new_locator)
                    for spine in ax.spines.values():
                        spine.set_linewidth(ss.LINE_WIDTH)
                    ax.set(
                        xticks=[],
                        yticks=[],
                        xlim=xlim,
                        ylim=ylim
                    )
                    ax.tick_params(
                        axis="both",
                        labelsize=ss.TICK_LABEL_SIZE,
                        size=ss.TICK_SIZE
                    )
            i = r*ncols + c
            letter = chr(ord("a") + i % 26)
            if i >= 26:
                letter = letter + letter
            axs[r, c, 0, 0].text(
                0,
                letter_position,
                letter,
                fontsize=ss.LETTER_LABEL_SIZE,
                transform=axs[r, c, 0, 0].transAxes,
                weight="bold"
            )
            for a in range(0, nr, step):
                axs[r, c, a, 0].set(yticks=[ylim[1]/2], yticklabels=[])
            for e in range(0, nc, step):
                axs[r, c, -1, e].set(xticks=[xlim[1]/2], xticklabels=[])
        for a in range(0, nr, step):
            axs[r, 0, a, 0].set_yticklabels([y_values[a]])
    for c in range(ncols):
        axs[0, c, 0, int(nc/2)].set_title(
            column_titles[c],
            pad=ss.PLOT_SIZE * ss.TITLE_PADDING,
            fontsize=ss.LETTER_LABEL_SIZE
        )
        for e in range(0, nc, step):
            axs[-1, c, -1, e].set_xticklabels([f"{x_values[e]:.0f}"])
    for r in range(nrows):
        for a in range(0, nr, step):
            axs[r, -1, a, -1].annotate(
                row_titles[a],
                xy=(1, 0.5),
                xycoords="axes fraction",
                xytext=(ss.PLOT_SIZE * ss.TITLE_PADDING, 0),
                textcoords="offset points",
                va="center",
                ha="left",
                fontsize=ss.LETTER_LABEL_SIZE
            )

    return axs
