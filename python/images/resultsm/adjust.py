""" Adjust ax when there are 3 subplots """

from modules.add_ticks import add_ticklabels_ax


def adjust(axs):
    """Adjust ax when there are 3 subplots"""

    axs[1, 0, 0, 0].remove()
    ax = axs[0, 0, 0, 0]
    l, b, w, h = ax.get_position().bounds
    ax.set_axes_locator(None)
    ax.set_position((0.133, 0.3443, 0.213, 0.315))
    ax.set_title("No shuffling\n$\\mathit{s}_{\\mathit{1}}$, $\\mathit{s}_{\\mathit{3}}$", fontsize=32, pad=215)
    add_ticklabels_ax(ax, [0.1, 0, 0.9], [-31, 0, 0.97])
