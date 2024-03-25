#!/usr/bin/env python

import argparse
import numpy as np
import os
import pandas as pd
import re
import time

from matplotlib.animation import FuncAnimation
from matplotlib.cm import ScalarMappable
from matplotlib import colormaps
from mpl_toolkits.axes_grid1 import Divider, Size
import matplotlib.pyplot as plt
import matplotlib.transforms

import main_figures.settings as ss
import main_figures.modes as mm
from main_figures.get_df import get_df
from main_figures.update_Z import update_Z

def update(t, mode, df_mechanisms, dffrq_mechanisms, movie, text, artists): 
    alphas = np.sort(df_mechanisms["none"]["alpha"].unique())[::-1]
    logess = np.sort(df_mechanisms["none"]["logES"].unique())
    traits = mm.get_traits(mode)
    for r, mechanism in enumerate(df_mechanisms):
        if ("cooperation" in mode or "correlations" in mode or "test" in mode) and mechanism == "social":
            continue
        for c, trait in enumerate(traits):
            Z = update_Z(t, df_mechanisms, mechanism, trait, mode)
            for a, alpha in enumerate(alphas):
                for e, loges in enumerate(logess):
                    d = dffrq_mechanisms[mechanism][(dffrq_mechanisms[mechanism]["Time"] == t) & (dffrq_mechanisms[mechanism]["alpha"] == alpha) & (dffrq_mechanisms[mechanism]["logES"] == loges)]
                    freq_a = [col for col in d.columns if re.match(fr"^{trait}\d+$", col)]
                    y = d.loc[:, freq_a].values[0].flatten()
                    artists[r, c, a, e].set_ydata(y)
                    bgcolor = colormaps[ss.color_map]((Z[a, e] + 1) / 2)
                    artists[r, c, a, e].axes.set_facecolor(bgcolor)
    if movie:
        text.set_text(t)
    elif ss.print_folder:
        text.set_text(os.path.basename(os.getcwd()))
    else:
        text.set_text("")
    return artists.flatten()

def main(mode, movie):

    start_time = time.perf_counter()
    this_script = os.path.basename(__file__)
    script_name = this_script.split(".")[0]

    # Set figure properties

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    # Get data

    mechanisms = mm.get_mechanisms(mode)
    df_mechanisms = {}
    dffrq_mechanisms = {}

    for mechanism in mechanisms:
        df_mechanisms[mechanism] = get_df(mechanism, "csv", movie)
        dffrq_mechanisms[mechanism] = get_df(mechanism, "frq", movie)
    if "social" not in mechanisms:
        df_mechanisms["social"] = get_df("social", "csv", movie)
    df = df_mechanisms[mechanisms[0]]
    ts = df.Time.unique()
    nr = df.alpha.nunique()
    nc = df.logES.nunique()
    xlim = [-2, ss.bins + 1]
    ylim = [0, 0.25]
    step = int(nr/2)
    alphas = np.sort(df["alpha"].unique())[::-1]
    logess = np.sort(df["logES"].unique())
    letterposition = 1.0 + ss.letterposition * nr

    # Create figure

    traits = mm.get_traits(mode)
    ncols = len(traits)
    nrows = len(mechanisms)
    inner_width = ss.plotsize*ncols + ss.spacing*(ncols - 1)
    inner_height = ss.plotsize*nrows + ss.spacing*(nrows - 1)
    width = inner_width + ss.left_margin + ss.right_margin
    height = inner_height + ss.top_margin + ss.bottom_margin

    fig = plt.figure(figsize=(width, height))
    fig.supxlabel(ss.xlabel,
                  x=(ss.left_margin + inner_width/2)/width,
                  y=(ss.bottom_margin - ss.xlabel_padding)/height,
                  fontsize=ss.biglabel)
    fig.supylabel(ss.ylabel,
                  x=(ss.left_margin - ss.ylabel_padding)/width,
                  y=(ss.bottom_margin + inner_height/2)/height,
                  fontsize=ss.biglabel)
    fig.text((ss.left_margin + inner_width)/width,
             (ss.bottom_margin - ss.xlabel_padding)/height,
             "",
             fontsize=ss.ticklabel,
             color="grey",
             ha="right")

    plotsize_fixed = Size.Fixed(ss.plotsize/nc)
    spacing_fixed = Size.Fixed(ss.spacing)
    divider = Divider(fig,
                      (ss.left_margin/width,
                       ss.bottom_margin/height,
                       inner_width/width,
                       inner_height/height),
                      [plotsize_fixed] * nc + ([spacing_fixed] + [plotsize_fixed] * nc) * (ncols - 1),
                      [plotsize_fixed] * nr + ([spacing_fixed] + [plotsize_fixed] * nr) * (nrows - 1),
                      aspect=False)

    outergrid = fig.add_gridspec(nrows=nrows,
                                 ncols=ncols)
    axs = np.empty((nrows,
                    ncols,
                    nr,
                    nc),
                    dtype=object)

    for r, _ in enumerate(mechanisms):
        for c, _ in enumerate(traits):
            grid = outergrid[r, c].subgridspec(nrows=nr,
                                               ncols=nc,
                                               hspace=0.0,
                                               wspace=0.0)
            axs[r, c] = grid.subplots()
            for a in range(nr):
                inner_y = (nrows - r - 1) * (nr + 1) + nr - a - int(a / nr) - 1
                for e in range(nc):
                    inner_x = c * (nc + 1) + e + int(e / nc)
                    axs[r, c, a, e].set_axes_locator(divider.new_locator(nx=inner_x, ny=inner_y))
                    for spine in axs[r, c, a, e].spines.values():
                        spine.set_linewidth(ss.linewidth)
                    axs[r, c, a, e].set(xticks=[],
                                        yticks=[],
                                        xlim=xlim,
                                        ylim=ylim)
                    axs[r, c, a, e].tick_params(axis="both",
                                                labelsize=ss.ticklabel,
                                                size=ss.ticksize)
            i = r*ncols + c
            letter = chr(ord("a") + i % 26)
            if i >= 26:
                letter = letter + letter
            axs[r, c, 0, 0].text(0,
                                 letterposition,
                                 letter,
                                 fontsize=ss.letterlabel,
                                 transform=axs[r, c, 0, 0].transAxes,
                                 weight="bold")
            for a in range(0, nr, step):
                axs[r, c, a, 0].set(yticks=[ylim[1]/2], yticklabels=[])
            for e in range(0, nc, step):
                axs[r, c, -1, e].set(xticks=[xlim[1]/2], xticklabels=[])
        for a in range(0, nr, step):
            axs[r, 0, a, 0].set_yticklabels([alphas[a]])
    for c, trait in enumerate(traits):
        axs[0, c, 0, int(nc/2)].set_title(mm.get_title(trait),
                                          pad=ss.plotsize * ss.titlepad,
                                          fontsize=ss.letterlabel)
        for e in range(0, nc, step):
            axs[-1, c, -1, e].set_xticklabels([f"{logess[e]:.0f}"])

    # Assign axs objects to variables
    # (Line2D)

    artists = np.empty_like(axs) 
    x = np.arange(ss.bins)
    dummy_y = np.zeros_like(x)

    for r, _ in enumerate(mechanisms):
        for c, _ in enumerate(traits):
            for a, _ in enumerate(alphas):
                for e, _ in enumerate(logess):
                    ax = axs[r, c, a, e] 
                    artists[r, c, a, e], = ax.plot(x, dummy_y, c="black", lw=ss.linewidth * 2)

    sm = ScalarMappable(cmap=ss.color_map, norm=plt.Normalize(-1, 1))
    cax = fig.add_axes([(ss.left_margin + inner_width + ss.spacing)/width,
                        (ss.bottom_margin + inner_height/2 - ss.plotsize/2)/height,
                        (ss.plotsize/nc)/width,
                        ss.plotsize/height]) # [left, bottom, width, height]
    cbar = fig.colorbar(sm,
                        cax=cax,
                        ticks=[-1, 0, 1])
    cbar.ax.tick_params(labelsize=ss.ticklabel, size=ss.ticksize)
    cbar.outline.set_linewidth(ss.linewidth)

    # Save figure

    name = f"{script_name}_{mode}"
    if movie:
        ani = FuncAnimation(fig,
                            update,
                            frames=ts,
                            fargs=(mode,
                                   df_mechanisms,
                                   dffrq_mechanisms,
                                   movie,
                                   fig.texts[2],
                                   artists,),
                            blit=True)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        update(ts[-1],
               mode,
               df_mechanisms,
               dffrq_mechanisms,
               movie,
               fig.texts[2],
               artists,)
        plt.savefig(f"{name}.png", transparent=False)
    plt.close()

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Results plots",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("mode", help="Mode: demography or cooperation")
    parser.add_argument("movie", nargs="?", default=False, help="Enable movie")
    args = parser.parse_args()

    main(args.mode, args.movie)

