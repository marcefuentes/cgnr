"""Add labels to plots."""


def add_ax_labels(ax, x_label, y_label, fontsize, labelpad):
    """Add labels to axes."""

    ax.set_xlabel(x_label, fontsize=fontsize, labelpad=labelpad)
    ax.set_ylabel(y_label, fontsize=fontsize, labelpad=labelpad)
