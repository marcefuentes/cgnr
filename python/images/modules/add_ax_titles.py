"""Add titles to plots."""


def add_ax_titles(ax, x_title, y_title, fontsize, labelpad):
    """Add titles to axes."""

    ax.set_xlabel(x_title, fontsize=fontsize, labelpad=labelpad)
    ax.set_ylabel(y_title, fontsize=fontsize, labelpad=labelpad)
