""" Format axes. """


def axes_format(image):
    """Format axes."""

    axs = image["axs"]

    # Format spines

    for ax in axs.flatten():
        for spine in ax.spines.values():
            spine.set(**image["spines"])

    # Set limits and reset ticks

    params = {
        "xlim": image["lim_x"],
        "ylim": image["lim_y"],
        "xticks": [],
        "yticks": [],
    }
    for ax in axs.flatten():
        ax.set(**params)

    # Add titles

    nrows, ncols, nr, nc = axs.shape

    for j in range(ncols):
        axs[0, j, 0, int(nc / 2)].set_title(
            image["titles_columns"][j], **image["titles_columns_params"]
        )

    for i in range(nrows):
        axs[i, -1, int(nr / 2), -1].annotate(
            image["titles_rows"][i], **image["titles_rows_params"]
        )
