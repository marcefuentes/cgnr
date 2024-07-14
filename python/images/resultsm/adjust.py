""" Adjust ax when there are 3 subplots """

from modules.add_ticks import add_ticklabels_ax


def adjust(axs):
    """Adjust ax when there are 3 subplots"""

    axs[1, 0, 0, 0].remove()
    ax = axs[0, 0, 0, 0]
    l, b, w, h = ax.get_position().bounds
    ax.set_axes_locator(None)
    # new_position = [l - 0.035, b * 0.603, w * 1.05, h * 1.05]
    new_position = [l + 0.04833, b * 0.667, w * 0.833, h * 0.833]
    ax.set_position(new_position)
    ax.set_title("No shuffling\n$\\mathit{s}_{\\mathit{1}}$, $\\mathit{s}_{\\mathit{3}}$", fontsize=32, pad=215)
    add_ticklabels_ax(ax, [0.1, 0, 0.9], [-31, 0, 0.97])
