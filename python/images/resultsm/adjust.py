""" Adjust ax when there are 3 subplots """

from modules.add_ticks import add_ticklabels_ax


def adjust(axs, layout):
    """Adjust the plots"""

    if layout == "m03" or layout == "m05" or layout == "m07":
        adjust1(axs)
    elif layout == "m10":
        adjust2(axs)


def adjust1(axs):
    """Adjust a single plot"""

    axs[1, 0, 0, 0].remove()
    ax = axs[0, 0, 0, 0]
    ax.set_axes_locator(None)
    ax.set_position((0.133, 0.3433, 0.213, 0.315))
    ax.set_title(
        "No shuffling\n$\\mathit{s}_{\\mathit{1}}$, $\\mathit{s}_{\\mathit{3}}$",
        fontsize=32,
        pad=215,
    )
    add_ticklabels_ax(ax, [0.9, 0.5, 0.1], [-31, 0, 0.97])


def adjust2(axs):
    """Adjust two plots"""

    axs[1, 0, 0, 0].remove()
    ax = axs[0, 0, 0, 0]
    ax.set_axes_locator(None)
    ax.set_position((0.133, 0.5473, 0.213, 0.315))  # for 1 row
    ax.set_title(
        "No shuffling\n$\\mathit{s}_{\\mathit{1}}$, $\\mathit{s}_{\\mathit{3}}$",
        fontsize=32,
        pad=215,
    )
    add_ticklabels_ax(ax, [0.9, 0.5, 0.1], ["", "", ""])

    axs[3, 0, 0, 0].remove()
    ax = axs[2, 0, 0, 0]
    ax.set_axes_locator(None)
    ax.set_position((0.133, 0.1373, 0.213, 0.315))  # for 1 row
    add_ticklabels_ax(ax, [0.9, 0.5, 0.1], [-31, 0, 0.97])
