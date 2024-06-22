""" Increase the length of the middle tick of a given axis. """


def enlarge_ticks(axs, options, margin_inner):
    """Increase the length of the middle tick of a given axis."""

    if options["layout"] == "allp":
        if options["trait"] == "ChooseGrainmean":
            axs_to_change = [
                (axs[1, 0, 0, 0], "x"),
                (axs[1, 1, 0, 0], "y"),
                (axs[1, 1, 0, 0], "x"),
                (axs[1, 2, 0, 0], "y"),
                (axs[1, 2, 0, 0], "x"),
                (axs[1, 3, 0, 0], "y"),
                (axs[1, 3, 0, 0], "x"),
                (axs[2, 1, 0, 0], "y"),
                (axs[2, 2, 0, 0], "y"),
                (axs[2, 3, 0, 0], "y"),
            ]
        if options["trait"] == "MimicGrainmean" and not options["lang"]:
            axs_to_change = [
                (axs[0, 1, 0, 0], "y"),
                (axs[0, 2, 0, 0], "y"),
                (axs[0, 3, 0, 0], "y"),
                (axs[1, 0, 0, 0], "x"),
                (axs[1, 1, 0, 0], "y"),
                (axs[1, 1, 0, 0], "x"),
                (axs[2, 1, 0, 0], "y"),
            ]
        if options["trait"] == "MimicGrainmean" and options["lang"]:
            axs_to_change = [
                (axs[1, 1, 0, 0], "y"),
            ]
        if options["trait"] == "ImimicGrainmean" and not options["lang"]:
            axs_to_change = [
                (axs[0, 0, 0, 0], "x"),
                (axs[0, 1, 0, 0], "y"),
                (axs[0, 2, 0, 0], "y"),
                (axs[0, 3, 0, 0], "y"),
                (axs[0, 1, 0, 0], "x"),
                (axs[0, 2, 0, 0], "x"),
                (axs[0, 3, 0, 0], "x"),
                (axs[1, 0, 0, 0], "x"),
                (axs[1, 1, 0, 0], "y"),
                (axs[1, 2, 0, 0], "y"),
                (axs[1, 3, 0, 0], "y"),
                (axs[1, 1, 0, 0], "x"),
                (axs[2, 0, 0, 0], "x"),
                (axs[2, 1, 0, 0], "y"),
                (axs[2, 1, 0, 0], "x"),
                (axs[3, 1, 0, 0], "y"),
                (axs[3, 2, 0, 0], "y"),
                (axs[3, 3, 0, 0], "y"),
            ]

        for ax in axs_to_change:
            if ax[1] == "x":
                ticks = ax[0].xaxis.get_major_ticks()
            if ax[1] == "y":
                ticks = ax[0].yaxis.get_major_ticks()

            ticks[len(ticks) // 2].tick1line.set_markersize(margin_inner * 72)
