#!/usr/bin/env python

import os
import time

from matplotlib import cm
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import numpy as np

from modules.parse_args import parse_args
from modules.prettify_axes import prettify_plot_axes
from modules.init_artists import init_plot_artists
from modules.init_fig import init_fig
from common_modules.get_config import get_config
from analytic_figures.modules.process_plt import process_plt, close_plt
import modules.settings as ss
from modules.update import update_artists
from modules.get_data import get_data

# Add data to figure

def main(args):
    """Main function"""

    start_time = time.perf_counter()
    this_file = os.path.basename(__file__)
    file_name = this_file.split(".")[0]

    givens, update_args = get_data()

    axes_args = {
        "x_values": update_args["logess"],
        "y_values": update_args["alphas"],
    }

    update_args["movie"] = args.movie

    fig_args = {
        "nrows": 1,
        "ncols": 2,
        "nr": len(update_args["alphas"]),
        "nc": len(update_args["logess"]),
        "nested": True,
    }

    fig, axes_args["axs"], axes_args["divider"] = init_fig(fig_args)
    prettify_plot_axes(axes_args)

    update_args["budgets"], update_args["icurves"] = init_plot_artists(axes_args["axs"], update_args)

    # Add colorbar
    norm = Normalize(vmin=0, vmax=1)
    axins = inset_axes(axes_args["axs"][0, -1, -1],
        width="5%",
        height="100%",
        loc="upper right",
        bbox_to_anchor=(880, 200, 200, 200),
        borderpad=0)
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap="Reds"),
        cax=axins,
        ticks=[0, 0.5, 1])
    cbar.ax.tick_params(labelsize=ss.TICK_LABEL_SIZE)
    cbar.outline.set_linewidth(0.2)

    # Add data and save figure

    process_plt(fig, givens, update_args, file_name)

    close_plt(fig)

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")

if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
