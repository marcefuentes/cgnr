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
from common_modules.get_config import get_config
from analytic_figures.modules.process_plt import process_plt, close_plt
import modules.settings as ss
from modules.update import update_artists
from modules.get_data import get_data

start_time = time.perf_counter()
this_file = os.path.basename(__file__)
file_name = this_file.split(".")[0]

# Options

givens = np.linspace(0.0, 1.0, num=21)
givens = [0.0]

num = 3     # Number of subplot rows & columns
numqB = 256 # Number of points along each curve
n_ic = 5    # Number of indifference curves

plotsize = 6

# Add data to figure

def main(args):
    """Main function"""

    givens, update_args = get_data()

    update_args["movie"] = args.movie

    axs_args = {
        "y_values": update_args["alphas"],
        "x_values": update_args["logess"],
    }

    norm = Normalize(vmin=0, vmax=1)

    # Figure properties

    width = plotsize*2
    height = plotsize
    xlabel = "Substitutability of $\it{B}$"
    ylabel = "Influence of $\it{B}$"
    biglabel = plotsize*4
    ticklabel = plotsize*3
    xlim=[0.0, 1.0]
    ylim=[0.0, 1.0]
    step = int(num/2)
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    # Create figure

    axs = np.empty((2,
            len(axs_args["y_values"]),
            len(axs_args["x_values"])),
        dtype=object)

    fig = plt.figure(figsize=(width, height))
    outergrid = fig.add_gridspec(nrows=1,
        ncols=2,
        left=0.15,
        right=0.85,
        top=0.8,
        bottom=0.2)
    for g in range(2):
        grid = outergrid[g].subgridspec(nrows=num,
            ncols=num,
            wspace=0,
            hspace=0)
        axs[g] = grid.subplots()

    left_x = axs[0, 0, 0].get_position().x0
    right_x = axs[-1, -1, -1].get_position().x1
    center_x = (left_x + right_x) / 2
    top_y = axs[0, 0, 0].get_position().y1
    bottom_y = axs[-1, -1, -1].get_position().y0
    center_y = (top_y + bottom_y) / 2
    fig.supxlabel(xlabel,
        x=center_x,
        y=bottom_y*0.3,
        fontsize=biglabel)
    fig.supylabel(ylabel,
        x=left_x*0.4,
        y=center_y,
        fontsize=biglabel)

    for ax in fig.get_axes():
        ax.set(xticks=[], yticks=[])
        ax.set(xlim=xlim, ylim=ylim)
        for axis in ["top","bottom","left","right"]:
            ax.spines[axis].set_linewidth(0.2)

    for g in range(2):
        letter = ord("a") + g
        axs[g, 0, 0].set_title(chr(letter),
            fontsize=plotsize*5,
            weight="bold",
            loc="left")
        if g == 0:
            for a in range(0, num, step):
                axs[g, a, 0].set_ylabel(f"{axs_args['y_values'][a]:.1f}",
                    rotation="horizontal",
                    horizontalalignment="right",
                    verticalalignment="center",
                    fontsize=ticklabel)
        for r in range(0, num, step):
            axs[g, -1, r].set_xlabel(f"{axs_args['x_values'][r]:.0f}",
                fontsize=ticklabel)

    # Assign axs objects to variables
    # (Line2D)

    budgets = np.empty_like(axs)
    icurves = np.empty_like(axs)
    dummy_budgety = np.full_like(update_args["icx"], -1.0)
    dummy_icy = np.zeros_like(update_args["icx"])

    for g in range(2):
        for a, alpha in enumerate(update_args["alphas"]):
            for r, rho in enumerate(update_args["rhos"]):
                if g == 0:
                    for c in range(n_ic): 
                        axs[0, a, r].plot(update_args["icx"], update_args["isoclines"][a, r, c], c="0.850")
                budgets[g, a, r], = axs[g, a, r].plot(update_args["icx"],
                    dummy_budgety,
                    c="0.300",
                    linewidth=4,
                    alpha=0.8)
                icurves[g, a, r], = axs[g, a, r].plot(update_args["icx"],
                    dummy_icy,
                    linewidth=4,
                    alpha=0.8)
    update_args["budgets"] = budgets
    update_args["icurves"] = icurves

    # Add colorbar
    axins = inset_axes(axs[0, -1, -1],
        width="5%",
        height="100%",
        loc="upper right",
        bbox_to_anchor=(880, 200, 200, 200),
        borderpad=0)
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap="Reds"),
        cax=axins,
        ticks=[0, 0.5, 1])
    cbar.ax.tick_params(labelsize=ticklabel)
    cbar.outline.set_linewidth(0.2)

    # Add data and save figure

    process_plt(fig, givens, update_args, file_name)

    close_plt(fig)

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")

if __name__ == "__main__":
    parsed_args = parse_args()
    main(parsed_args)
