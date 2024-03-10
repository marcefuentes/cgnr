#! /usr/bin/env python

import argparse
import numpy as np
import os
import time

from matplotlib.animation import FuncAnimation
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
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

    # Set figure properties

    color_map = "RdBu_r"
    plotsize = 4
    width = plotsize*len(titles)
    height = plotsize*len(rows)
    fig_left = 0.12
    fig_right = 0.88
    fig_top = 0.88
    fig_bottom = 0.12
    fig_wspace = 0.2
    fig_hspace = 0.2
    bar_height = 0.2
    bar_width = 0.01
    xlabel = "Substitutability of $\it{B}$"
    ylabel = "Influence of $\it{B}$"
    biglabel = plotsize*7
    letterlabel = plotsize*6
    ticklabel = plotsize*5
    xticks = [0, nc/2 - 0.5, nc - 1]
    yticks = [0, nr/2 - 0.5, nr - 1]
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
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    # Create figure

    fig, main_ax = plt.subplots(nrows=len(rows),
                            ncols=len(titles),
                            figsize=(width, height))

    axs = main_ax if len(rows) > 1 else main_ax[np.newaxis, :]
    fig.subplots_adjust(left=fig_left,
                        right=fig_right,
                        top=fig_top,
                        bottom=fig_bottom,
                        wspace=fig_wspace,
                        hspace=fig_hspace)

    fig.supxlabel(xlabel,
                  x=(fig_left + fig_right) * 0.5,
                  y=fig_bottom - 0.04*biglabel/height,
                  fontsize=biglabel)
    fig.supylabel(ylabel,
                  x=fig_left - 0.05*biglabel/width,
                  y=(fig_bottom + fig_top) * 0.5,
                  fontsize=biglabel)

    letterposition = 1.035
    for i, ax in enumerate(fig.get_axes()):
        ax.set(xticks=xticks, yticks=yticks)
        ax.set(xticklabels=[], yticklabels=[])
        for axis in ["top", "bottom", "left", "right"]:
            ax.spines[axis].set_linewidth(0.1)
        letter = ord("a") + i
        ax.text(0,
                letterposition,
                chr(letter),
                transform=ax.transAxes,
                fontsize=letterlabel,
                weight="bold")
    for r, row in enumerate(rows):
        axs[r, 0].set_yticklabels(yticklabels, fontsize=ticklabel)
    for c, title in enumerate(titles):
        axs[0, c].set_title(title, pad=plotsize*10, fontsize=letterlabel)
        axs[-1, c].set_xticklabels(xticklabels, fontsize=ticklabel)
    fig.text(fig_right,
             fig_bottom * 0.5,
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
    cax = fig.add_axes([0.5 * (1 - bar_width + fig_right),
                        0.5 * (1 - bar_height),
                        bar_width,
                        bar_height]) # [left, bottom, width, height]
    cbar = fig.colorbar(sm,
                        cax=cax,
                        ticks=[-1, 0, 1])
    cbar.ax.tick_params(labelsize=ticklabel)
    cbar.outline.set_linewidth(0.1)

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
