#! /usr/bin/env python

import argparse
import os
import numpy as np
import pandas as pd
import re
import time

from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.transforms

from myget_df import get_df
from mytraits import ttr
from myupdate_Z import update_Z

def update(t, traitset, df_dict, dffrq_dict, movie, text, artists): 
    alphas = df_dict["none"]["alpha"].unique()
    logess = df_dict["none"]["logES"].unique()
    traits, _, _ = ttr(traitset)
    for r, key in enumerate(df_dict):
        if ("cooperation" in traitset or "correlations" in traitset) and key == "social":
            continue
        for c, trait in enumerate(traits):
            Z = update_Z(t, df_dict, key, trait, traitset)

            for a, alpha in enumerate(alphas):
                for e, loges in enumerate(logess):
                    d = dffrq_dict[key][(dffrq_dict[key]["alpha"] == alpha) & (dffrq_dict[key]["logES"] == loges)]
                    freq_a = [col for col in d.columns if re.match(fr"^{trait}\d+$", col)]
                    y = d.loc[:, freq_a].values[0].flatten()
                    artists[r, c, a, e].set_ydata(y)
                    bgcolor = cm.RdBu_r((Z[a, e] + 1) / 2)
                    artists[r, c, a, e].axes.set_facecolor(bgcolor)
    if movie:
        text.set_text(t)
    else:
        #text.set_text(os.path.basename(os.getcwd()))
        text.set_text("")

    return artists.flatten()

def main(traitset, movie):

    #this_file = os.path.basename(__file__)
    #file_name = this_file.split(".")[0]

    _, titles, rows = ttr(traitset)

    # Get data

    df_dict = {}
    dffrq_dict = {}

    for row in rows:
        df_dict[row] = get_df(row, "csv", movie)
        dffrq_dict[row] = get_df(row, "frq", movie)
    if "social" not in rows:
        df_dict["social"] = get_df("social", "csv", movie)
    df = df_dict[rows[0]]
    ts = df.Time.unique()
    nr = df.alpha.nunique()
    nc = df.logES.nunique()
    alphas = np.sort(pd.unique(df.alpha))[::-1]
    logess = np.sort(pd.unique(df.logES))

    # Set figure properties

    bins = 64
    plotsize = 4
    width = plotsize*len(titles)
    height = plotsize*len(rows)
    xlabel = "Substitutability of $\it{B}$"
    ylabel = "Influence of $\it{B}$"
    biglabel = plotsize*7
    letterlabel = plotsize*6
    ticklabel = plotsize*5
    xlim = [-2, bins + 1]
    ylim = [0, 0.25]
    step = int(nr/2)
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    # Create figure

    axs = np.empty((len(rows),
                    len(titles),
                    nr,
                    nc),
                    dtype=object)

    fig = plt.figure(figsize=(width, height))
    outergrid = fig.add_gridspec(nrows=len(rows),
                                 ncols=len(titles))
    for r, row in enumerate(rows):
        for c, title in enumerate(titles):
            grid = outergrid[r, c].subgridspec(nrows=nr,
                                               ncols=nc,
                                               wspace=0,
                                               hspace=0)
            axs[r, c] = grid.subplots()

    left_x = axs[0, 0, 0, 0].get_position().x0
    right_x = axs[-1, -1, -1, -1].get_position().x1
    center_x = (left_x + right_x) / 2
    top_y = axs[0, 0, 0, 0].get_position().y1
    bottom_y = axs[-1, -1, -1, -1].get_position().y0
    center_y = (top_y + bottom_y) / 2
    fig.supxlabel(xlabel,
                  x=center_x,
                  y=bottom_y - 1.2/height,
                  fontsize=biglabel)
    fig.supylabel(ylabel,
                  x=left_x - 1.45/width,
                  y=center_y,
                  fontsize=biglabel)

    for ax in fig.get_axes():
        ax.set(xticks=[], yticks=[])
        ax.set(xlim=xlim, ylim=ylim)
        for axis in ["top", "bottom", "left", "right"]:
            ax.spines[axis].set_linewidth(0.1)

    for r, row in enumerate(rows):
        for c, title in enumerate(titles):
            letter = ord("a") + r*len(titles) + c
            axs[r, c, 0, 0].set_title(chr(letter),
                                      fontsize=letterlabel,
                                      pad = 10,
                                      weight="bold",
                                      loc="left")
            if r == 0:
                axs[0, c, 0, 10].set_title(title,
                                           pad=plotsize*9,
                                           fontsize=letterlabel)
            for a in range(0, nr, step):
                axs[r, c, a, 0].set(yticks=[ylim[1]/2.0], yticklabels=[])
                if c == 0:
                    axs[r, 0, a, 0].set_yticklabels([alphas[a]],
                                                    fontsize=ticklabel)
            for e in range(0, nc, step):
                axs[r, c, -1, e].set(xticks=[xlim[1]/2.0], xticklabels=[])
                if row == rows[-1]:
                    axs[-1, c, -1, e].set_xticklabels([f"{logess[e]:.0f}"],
                                                     fontsize=ticklabel)
    fig.text(right_x,
             bottom_y*0.5,
             "t\n0",
             fontsize=biglabel,
             color="grey",
             ha="right")

    # Assign axs objects to variables
    # (Line2D)

    artists = np.empty_like(axs) 
    x = np.arange(bins)
    dummy_y = np.zeros_like(x)
    frames = ts

    for r, row in enumerate(rows):
        for c, title in enumerate(titles):
            for a, alpha in enumerate(alphas):
                for e, loges in enumerate(logess):
                    ax = axs[r, c, a, e] 
                    artists[r, c, a, e], = ax.plot(x, dummy_y, c="black", lw=0.1)

    fig_x, fig_y = fig.get_size_inches() * fig.dpi  # Convert figure size to pixels

    right_x_pixels = right_x * fig_x
    center_y_pixels = center_y * fig_y

    sm = plt.cm.ScalarMappable(cmap="RdBu_r", norm=plt.Normalize(vmin=-1, vmax=1))
    sm._A = []  # Set empty values

    axins = inset_axes(axs[-1, -1, -1, -1],
                       width="5%",
                       height="100%",
                       loc="upper right",
                       bbox_to_anchor=(0.847*right_x_pixels, 0.681*center_y_pixels, 300, 500),
                       borderpad=0)
    cbar = fig.colorbar(sm,
                        cax=axins,
                        ticks=[-1, 0, 1])
    cbar.ax.tick_params(labelsize=ticklabel)
    cbar.outline.set_linewidth(0.1)

    # Save figure

    name = f"{traitset}_frq"
    if movie:
        ani = FuncAnimation(fig,
                            update,
                            frames=ts,
                            fargs=(traitset,
                                   df_dict,
                                   dffrq_dict,
                                   movie,
                                   fig.texts[2],
                                   artists,),
                            blit=True)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        update(ts[-1],
               traitset,
               df_dict,
               dffrq_dict,
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
