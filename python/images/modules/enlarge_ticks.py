""" Increase the length of the middle tick of a given axis. """


def enlarge_ticks(axs, options, margin_inner, linewidth):
    """Increase the length of the middle tick of a given axis."""

    if options["layout"] == "allp":
        axs_to_change = []
        if options["lang"]:
            if "Choose" in options["trait"]:
                axs_to_change = [
                    (axs[1, 0, 0, 0], "x"),
                    (axs[1, 1, 0, 0], "y"),
                    (axs[1, 1, 0, 0], "x"),
                    (axs[2, 1, 0, 0], "y"),
                    (axs[1, 2, 0, 0], "y"),
                    (axs[1, 2, 0, 0], "x"),
                    (axs[1, 3, 0, 0], "y"),
                    (axs[1, 3, 0, 0], "x"),
                    (axs[2, 2, 0, 0], "y"),
                    (axs[2, 3, 0, 0], "y"),
                ]
            elif options["trait"] == "MimicGrainmean":
                axs_to_change = [
                    (axs[0, 1, 0, 0], "y"),
                    (axs[0, 2, 0, 0], "y"),
                    (axs[0, 3, 0, 0], "y"),
                    (axs[1, 1, 0, 0], "y"),
                    (axs[2, 1, 0, 0], "y"),
                ]
            elif "Imimic" in options["trait"]:
                axs_to_change = [
                    (axs[0, 0, 0, 0], "x"),
                    (axs[0, 1, 0, 0], "y"),
                    (axs[0, 1, 0, 0], "x"),
                    (axs[0, 2, 0, 0], "y"),
                    (axs[0, 2, 0, 0], "x"),
                    (axs[0, 3, 0, 0], "y"),
                    (axs[0, 3, 0, 0], "x"),
                    (axs[1, 1, 0, 0], "y"),
                    (axs[1, 2, 0, 0], "y"),
                    (axs[1, 3, 0, 0], "y"),
                    (axs[2, 1, 0, 0], "y"),
                    (axs[3, 1, 0, 0], "y"),
                    (axs[3, 2, 0, 0], "y"),
                    (axs[3, 3, 0, 0], "y"),
                ]
        else:
            axs_to_change = [
                (axs[1, 0, 0, 0], "x"),
                (axs[1, 1, 0, 0], "y"),
                (axs[1, 1, 0, 0], "x"),
                (axs[2, 1, 0, 0], "y"),
            ]
            if options["trait"] == "ChooseGrainmean":
                    axs_to_change.append((axs[1, 2, 0, 0], "y"))
                    axs_to_change.append((axs[1, 2, 0, 0], "x"))
                    axs_to_change.append((axs[1, 3, 0, 0], "y"))
                    axs_to_change.append((axs[1, 3, 0, 0], "x"))
                    axs_to_change.append((axs[2, 2, 0, 0], "y"))
                    axs_to_change.append((axs[2, 3, 0, 0], "y"))
            elif options["trait"] == "MimicGrainmean":
                    axs_to_change.append((axs[0, 1, 0, 0], "y"))
                    axs_to_change.append((axs[0, 2, 0, 0], "y"))
                    axs_to_change.append((axs[0, 3, 0, 0], "y"))
            elif options["trait"] == "ImimicGrainmean":
                    axs_to_change.append((axs[0, 0, 0, 0], "x"))
                    axs_to_change.append((axs[0, 1, 0, 0], "y"))
                    axs_to_change.append((axs[0, 2, 0, 0], "y"))
                    axs_to_change.append((axs[0, 3, 0, 0], "y"))
                    axs_to_change.append((axs[0, 1, 0, 0], "x"))
                    axs_to_change.append((axs[0, 2, 0, 0], "x"))
                    axs_to_change.append((axs[0, 3, 0, 0], "x"))
                    axs_to_change.append((axs[1, 2, 0, 0], "y"))
                    axs_to_change.append((axs[1, 3, 0, 0], "y"))
                    axs_to_change.append((axs[2, 0, 0, 0], "x"))
                    axs_to_change.append((axs[2, 1, 0, 0], "x"))
                    axs_to_change.append((axs[3, 1, 0, 0], "y"))
                    axs_to_change.append((axs[3, 2, 0, 0], "y"))
                    axs_to_change.append((axs[3, 3, 0, 0], "y"))

        for ax in axs_to_change:
            if ax[1] == "x":
                ticks = ax[0].xaxis.get_major_ticks()
            if ax[1] == "y":
                ticks = ax[0].yaxis.get_major_ticks()

            ticks[len(ticks) // 2].tick1line.set_markersize(margin_inner * 72)
            ticks[len(ticks) // 2].tick1line.set_markeredgewidth(linewidth * 4)
