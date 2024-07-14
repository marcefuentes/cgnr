""" Adjust ax when there are 3 subplots """

from modules.add_ticks import add_ticklabels_ax


def adjust1(axs):
    """Adjust a single plot"""

    axs[1, 0, 0, 0].remove()
    ax = axs[0, 0, 0, 0]
    ax.set_axes_locator(None)
    ax.set_position((0.133, 0.3443, 0.213, 0.315))
    ax.set_title("No shuffling\n$\\mathit{s}_{\\mathit{1}}$, $\\mathit{s}_{\\mathit{3}}$", fontsize=32, pad=215)
    add_ticklabels_ax(ax, [0.1, 0, 0.9], [-31, 0, 0.97])


def adjust2(axs):
    """Adjust two plots"""

    axs[1, 0, 0, 0].remove()
    ax = axs[0, 0, 0, 0]
    l, b, w, h = ax.get_position().bounds
    ax.set_axes_locator(None)
    ax.set_position((0.133, 0.5443, 0.213, 0.315)) # for 1 row
    ax.set_title("No shuffling\n$\\mathit{s}_{\\mathit{1}}$, $\\mathit{s}_{\\mathit{3}}$", fontsize=32, pad=215)

    axs[3, 0, 0, 0].remove()
    ax = axs[2, 0, 0, 0]
    l, b, w, h = ax.get_position().bounds
    ax.set_axes_locator(None)
    ax.set_position((0.133, 0.1443, 0.213, 0.315)) # for 1 row
    add_ticklabels_ax(ax, [0.1, 0, 0.9], [-31, 0, 0.97])
