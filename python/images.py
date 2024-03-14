#! /usr/bin/env python

import argparse
import numpy as np
import os
import time

from matplotlib.animation import FuncAnimation
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import Divider, Size
import matplotlib.pyplot as plt
import matplotlib.transforms

from myget_df import get_df
from mytraits import ttr
from myupdate_Z import update_Z

def update(t, traitset, df_dict, movie, text, artists): 
    traits, _, _ = ttr(traitset)
    for r, key in enumerate(df_dict):
        if ("cooperation" in traitset or "correlations" in traitset) and key == "social":
            continue
        for c, trait in enumerate(traits):
            Z = update_Z(t, df_dict, key, trait, traitset)
            artists[r, c].set_array(Z) 
    if movie:
        text.set_text(t)
    else:
        #text.set_text(os.path.basename(os.getcwd()))
        text.set_text("")

    return artists.flatten()

def main(traitset, movie):

    this_script = os.path.basename(__file__)
    script_name = this_script.split(".")[0]

    _, titles, rows = ttr(traitset)

    # Set figure properties

    color_map = "RdBu_r"
    plotsize = 4
    spacing = plotsize*0.75/4.0
    left_margin = plotsize*2.5/4.0
    right_margin = plotsize*2.5/4.0
    top_margin = plotsize*2.5/4.0
    bottom_margin = plotsize*2.5/4.0
    linewidth = plotsize*0.1/4.0
    xlabel = "Substitutability of $\it{B}$"
    ylabel = "Influence of $\it{B}$"
    xlabel_padding = plotsize*1.8/4.0
    ylabel_padding = plotsize*2.0/4.0
    biglabel = plotsize*9
    letterlabel = plotsize*8
    ticklabel = plotsize*6
    ticksize = plotsize*1.5

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    # Get data

    df_dict = {}

    for row in rows:
        df_dict[row] = get_df(row, "csv", movie)
    if "social" not in rows:
        df_dict["social"] = get_df("social", "csv", movie)
    df = df_dict[rows[0]]
    ts = df.Time.unique()
    nr = df.alpha.nunique()
    nc = df.logES.nunique()
    xticks = [0, 0.5*(nc - 1), nc - 1]
    yticks = [0, 0.5*(nr - 1), nr - 1]
    xmin = df.logES.min()
    xmax = df.logES.max()
    ymin = df.alpha.min()
    ymax = df.alpha.max()
    xticklabels = [f"{xmin:.0f}",
                   f"{(xmin + xmax)/2.:.0f}",
                   f"{xmax:.0f}"]
    yticklabels = [f"{ymax:.1f}",
                   f"{(ymin + ymax)/2.:.1f}",
                   f"{ymin:.1f}"]

    # Create figure

    inner_width = plotsize*len(titles) + spacing*(len(titles) - 1)
    inner_height = plotsize*len(rows) + spacing*(len(rows) - 1)
    width = inner_width + left_margin + right_margin
    height = inner_height + top_margin + bottom_margin

    fig, main_ax = plt.subplots(nrows=len(rows),
                                ncols=len(titles),
                                figsize=(width, height))

    plotsize_fixed = Size.Fixed(plotsize)
    spacing_fixed = Size.Fixed(spacing)
    divider = Divider(fig,
                      (left_margin/width,
                       bottom_margin/height,
                       inner_width/width,
                       inner_height/height),
                      [plotsize_fixed] + [spacing_fixed, plotsize_fixed] * (len(titles) - 1),
                      [plotsize_fixed] + [spacing_fixed, plotsize_fixed] * (len(rows) - 1),
                      aspect=False)
    for r, row in enumerate(rows):
        for c, title in enumerate(titles):
            main_ax[len(rows) - r - 1, c].set_axes_locator(divider.new_locator(nx=2*c, ny=2*r))
    axs = main_ax if len(rows) > 1 else main_ax[np.newaxis, :]

    fig.supxlabel(xlabel,
                  x=(left_margin + inner_width/2)/width,
                  y=(bottom_margin - xlabel_padding)/height,
                  fontsize=biglabel)
    fig.supylabel(ylabel,
                  x=(left_margin - ylabel_padding)/width,
                  y=(bottom_margin + inner_height/2)/height,
                  fontsize=biglabel)

    letterposition = 1.035
    for i, ax in enumerate(fig.get_axes()):
        ax.set(xticks=xticks, yticks=yticks)
        ax.tick_params(axis="both", labelsize=ticklabel, size=ticksize)
        ax.set(xticklabels=[], yticklabels=[])
        for axis in ["top", "bottom", "left", "right"]:
            ax.spines[axis].set_linewidth(linewidth)
        letter = ord("a") + i
        ax.text(0,
                letterposition,
                chr(letter),
                transform=ax.transAxes,
                fontsize=letterlabel,
                weight="bold")
    for r, row in enumerate(rows):
        axs[r, 0].set_yticklabels(yticklabels)
    for c, title in enumerate(titles):
        axs[0, c].set_title(title,
                            pad=plotsize * 10,
                            fontsize=letterlabel)
        axs[-1, c].set_xticklabels(xticklabels, fontsize=ticklabel)
    fig.text((left_margin + len(titles)*plotsize)/width,
             (bottom_margin - xlabel_padding)/height,
             "t\n0",
             fontsize=biglabel,
             color="grey",
             ha="right")

    # Assign axs objects to variables
    # (AxesImage)

    artists = np.empty_like(axs) 
    dummy_Z = np.zeros((nr, nc))

    for r, row in enumerate(rows):
        for c, title in enumerate(titles):
            artists[r, c] = axs[r, c].imshow(dummy_Z,
                                             cmap=color_map,
                                             vmin=-1,
                                             vmax=1)

    sm = ScalarMappable(cmap=color_map, norm=plt.Normalize(-1, 1))
    cax = fig.add_axes([(left_margin + inner_width + spacing)/width,
                        (bottom_margin + inner_height/2 - plotsize/2)/height,
                        (plotsize/nc)/width,
                        plotsize/height]) # [left, bottom, width, height]
    cbar = fig.colorbar(sm,
                        cax=cax,
                        ticks=[-1, 0, 1])
    cbar.ax.tick_params(labelsize=ticklabel)
    cbar.outline.set_linewidth(linewidth)

    # Save figure

    name = f"{script_name}_{traitset}"
    if movie:
        ani = FuncAnimation(fig,
                            update,
                            frames=ts,
                            fargs=(traitset,
                                   df_dict,
                                   movie,
                                   fig.texts[2],
                                   artists,),
                            blit=True)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        update(ts[-1],
               traitset,
               df_dict,
               movie,
               fig.texts[2],
               artists,)
        plt.savefig(f"{name}.png", transparent=False)
    plt.close()

if __name__ == "__main__":

    start_time = time.perf_counter()

    parser = argparse.ArgumentParser(description="Results plots",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("traitset", help="Trait set: demography or cooperation")
    parser.add_argument("movie", nargs="?", default=False, help="Enable movie")
    args = parser.parse_args()

    main(args.traitset, args.movie)

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")
