#! /usr/bin/env python

import argparse
import numpy as np
import os
import pandas as pd
import re
import time

from matplotlib.animation import FuncAnimation
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import Divider, Size
import matplotlib.pyplot as plt
import matplotlib.transforms
import matplotlib.cm as cm

import myfigure_settings as s
from myget_df import get_df
from mytraits import ttr
from myupdate_Z import update_Z

def update(t, traitset, df_dict, dffrq_dict, movie, text, artists): 
    alphas = np.sort(df_dict["none"]["alpha"].unique())[::-1]
    logess = np.sort(df_dict["none"]["logES"].unique())
    traits, _, _ = ttr(traitset)
    for r, key in enumerate(df_dict):
        if ("cooperation" in traitset or "correlations" in traitset or "test" in traitset) and key == "social":
            continue
        for c, trait in enumerate(traits):
            Z = update_Z(t, df_dict, key, trait, traitset)

            for a, alpha in enumerate(alphas):
                for e, loges in enumerate(logess):
                    d = dffrq_dict[key][(dffrq_dict[key]["Time"] == t) & (dffrq_dict[key]["alpha"] == alpha) & (dffrq_dict[key]["logES"] == loges)]
                    freq_a = [col for col in d.columns if re.match(fr"^{trait}\d+$", col)]
                    y = d.loc[:, freq_a].values[0].flatten()
                    artists[r, c, a, e].set_ydata(y)
                    bgcolor = cm.RdBu_r((Z[a, e] + 1) / 2)
                    artists[r, c, a, e].axes.set_facecolor(bgcolor)
    if movie:
        text.set_text(t)
    elif s.print_folder:
        text.set_text(os.path.basename(os.getcwd()))
    else:
        text.set_text("")

    return artists.flatten()

def main(traitset, movie):

    this_script = os.path.basename(__file__)
    script_name = this_script.split(".")[0]

    _, titles, rows = ttr(traitset)

    # Set figure properties

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

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
    xlim = [-2, s.bins + 1]
    ylim = [0, 0.25]
    step = int(nr/2)
    alphas = np.sort(df["alpha"].unique())[::-1]
    logess = np.sort(df["logES"].unique())

    # Create figure

    inner_width = s.plotsize*len(titles) + s.spacing*(len(titles) - 1)
    inner_height = s.plotsize*len(rows) + s.spacing*(len(rows) - 1)
    width = inner_width + s.left_margin + s.right_margin
    height = inner_height + s.top_margin + s.bottom_margin

    fig = plt.figure(figsize=(width, height))
    fig.supxlabel(s.xlabel,
                  x=(s.left_margin + inner_width/2)/width,
                  y=(s.bottom_margin - s.xlabel_padding)/height,
                  fontsize=s.biglabel)
    fig.supylabel(s.ylabel,
                  x=(s.left_margin - s.ylabel_padding)/width,
                  y=(s.bottom_margin + inner_height/2)/height,
                  fontsize=s.biglabel)
    fig.text((s.left_margin + inner_width)/width,
             (s.bottom_margin - s.xlabel_padding)/height,
             "",
             fontsize=s.ticklabel,
             color="grey",
             ha="right")

    plotsize_fixed = Size.Fixed(s.plotsize/nc)
    spacing_fixed = Size.Fixed(s.spacing)
    divider = Divider(fig,
                      (s.left_margin/width,
                       s.bottom_margin/height,
                       inner_width/width,
                       inner_height/height),
                      [plotsize_fixed] * nc + ([spacing_fixed] + [plotsize_fixed] * nc) * (len(titles) - 1),
                      [plotsize_fixed] * nr + ([spacing_fixed] + [plotsize_fixed] * nr) * (len(rows) - 1),
                      aspect=False)

    outergrid = fig.add_gridspec(nrows=len(rows),
                                 ncols=len(titles))
    axs = np.empty((len(rows),
                    len(titles),
                    nr,
                    nc),
                    dtype=object)

    for r, _ in enumerate(rows):
        for c, _ in enumerate(titles):
            grid = outergrid[r, c].subgridspec(nrows=nr,
                                               ncols=nc,
                                               hspace=0.0,
                                               wspace=0.0)
            axs[r, c] = grid.subplots()
    
    for r, _ in enumerate(rows):
        for c, _ in enumerate(titles):
            for a in range(nr):
                inner_y = (len(rows) - r - 1) * (nr + 1) + nr - a - int(a / nr) - 1
                for e in range(nc):
                    inner_x = c * (nc + 1) + e + int(e / nc)
                    axs[r, c, a, e].set_axes_locator(divider.new_locator(nx=inner_x, ny=inner_y))

    for ax in fig.get_axes():
        ax.set(xticks=[],
               yticks=[],
               xlim=xlim,
               ylim=ylim)
        ax.tick_params(axis="both",
                       labelsize=s.ticklabel,
                       size=s.ticksize)
        for spine in ax.spines.values():
            spine.set_linewidth(s.linewidth)

    letterposition = 1.0 + s.letterposition * nr
    for r, _ in enumerate(rows):
        for c, _ in enumerate(titles):
            letter = chr(ord("a") + r*len(titles) + c)
            axs[r, c, 0, 0].text(0,
                                 letterposition,
                                 letter,
                                 fontsize=s.letterlabel,
                                 transform=axs[r, c, 0, 0].transAxes,
                                 weight="bold")
    for ax, title in zip(axs[0, :], titles):
        ax[0, int(nc/2)].set_title(title,
                     pad=s.plotsize * 10,
                     fontsize=s.letterlabel)
    for r, _ in enumerate(rows):
        for c, _ in enumerate(titles):
            for a in range(0, nr, step):
                axs[r, c, a, 0].set(yticks=[ylim[1]/2.0], yticklabels=[])
            for e in range(0, nc, step):
                axs[r, c, -1, e].set(xticks=[xlim[1]/2.0], xticklabels=[])
    for r, _ in enumerate(rows):
        for a in range(0, nr, step):
            axs[r, 0, a, 0].set_yticklabels([alphas[a]])
    for c, _ in enumerate(titles):
        for e in range(0, nc, step):
            axs[-1, c, -1, e].set_xticklabels([f"{logess[e]:.0f}"])

    # Assign axs objects to variables
    # (Line2D)

    artists = np.empty_like(axs) 
    x = np.arange(s.bins)
    dummy_y = np.zeros_like(x)

    for r, _ in enumerate(rows):
        for c, _ in enumerate(titles):
            for a, _ in enumerate(alphas):
                for e, _ in enumerate(logess):
                    ax = axs[r, c, a, e] 
                    artists[r, c, a, e], = ax.plot(x, dummy_y, c="black", lw=s.linewidth * 2)

    sm = ScalarMappable(cmap=s.color_map, norm=plt.Normalize(-1, 1))
    cax = fig.add_axes([(s.left_margin + inner_width + s.spacing)/width,
                        (s.bottom_margin + inner_height/2 - s.plotsize/2)/height,
                        (s.plotsize/nc)/width,
                        s.plotsize/height]) # [left, bottom, width, height]
    cbar = fig.colorbar(sm,
                        cax=cax,
                        ticks=[-1, 0, 1])
    cbar.ax.tick_params(labelsize=s.ticklabel, size=s.ticksize)
    cbar.outline.set_linewidth(s.linewidth)

    # Save figure

    name = f"{script_name}_{traitset}"
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
