""" Adjust ax when there are 3 subplots """

from modules.add_ticks import add_ticklabels_ax


def adjust(axs, options, distances, image, ticklabels_x, ticklabels_y):
    """Adjust plots"""

    if options["layout"] in ("m03", "m05", "m06", "m10", "m16r"):

        nrows = len(options["variants"])
        ncols = len(options["variants"][0])

        left_0 = image["margin_left"]/distances["width"]
        top_ax = (image["margin_bottom"] + (image["plot_size"] + image["margin_inner"])*nrows/2.0)/distances["height"]

        axs[1, 0, 0, 0].remove()
        ax = axs[0, 0, 0, 0]
        ax.set_axes_locator(None)
        # new_position = (2.5/width, (2.5 + (4.0 + 0.75)*n - 4.0)/height, 4.0/width, 0.315)
        new_position = (left_0, top_ax, image["plot_size"]/distances["width"], 0.315)
        ax.set_position(new_position)

        if nrows == 2:
            add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)
            ax.set_title(options["titles_columns"][0], fontsize=32, pad=214)
        else:
            add_ticklabels_ax(ax, ticklabels_y, ["", "", ""])
                
            axs[2, 0, 0, 0].remove()
            ax = axs[3, 0, 0, 0]
            ax.set_axes_locator(None)
            bottom_ax = (image["margin_bottom"] + (image["plot_size"] + image["margin_inner"])*0.5)/distances["height"]
            #new_position = (2.5/width, (2.5 + (4.0 + 0.75)*n - 4.0)/height, 4.0/width, 0.315)
            new_position = (left_0, bottom_ax, image["plot_size"]/distances["width"], 0.315)
            ax.set_position(new_position)
            add_ticklabels_ax(ax, ticklabels_y, ticklabels_x)

            if ncols == 5:
                
                left_1 = left_0 + (image["plot_size"] + image["margin_inner"])/distances["width"]

                axs[1, 1, 0, 0].remove()
                ax = axs[0, 1, 0, 0]
                ax.set_axes_locator(None)
                n = 3
                # ax.set_position(((2.5 + 4.0 + 0.75)/width, (2.5 + (4.0 + 0.75)*n - 4.0)/height, 4.0/width, 0.315))
                ax.set_position((left_1, top_ax, image["plot_size"]/distances["width"], 0.315))
                ax.set_title(options["titles_columns"][1], fontsize=32, pad=214)

                axs[2, 1, 0, 0].remove()
                ax = axs[3, 1, 0, 0]
                ax.set_axes_locator(None)
                #ax.set_position(((2.5 + 4.0 + 0.75)/width, (2.5 + (4.0 + 0.75)*n - 4.0)/height, 4.0/width, 0.315))
                ax.set_position((left_1, bottom_ax, image["plot_size"]/distances["width"], 0.315))
                add_ticklabels_ax(ax, ["", "", ""], ticklabels_x)

