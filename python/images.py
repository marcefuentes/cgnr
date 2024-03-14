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

import myfigure_settings as s
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

    inner_width = s.plotsize*len(titles) + s.spacing*(len(titles) - 1)
    inner_height = s.plotsize*len(rows) + s.spacing*(len(rows) - 1)
    width = inner_width + s.left_margin + s.right_margin
    height = inner_height + s.top_margin + s.bottom_margin

    fig, main_ax = plt.subplots(nrows=len(rows),
                                ncols=len(titles),
                                figsize=(width, height))

    plotsize_fixed = Size.Fixed(s.plotsize)
    spacing_fixed = Size.Fixed(s.spacing)
    divider = Divider(fig,
                      (s.left_margin/width,
                       s.bottom_margin/height,
                       inner_width/width,
                       inner_height/height),
                      [plotsize_fixed] + [spacing_fixed, plotsize_fixed] * (len(titles) - 1),
                      [plotsize_fixed] + [spacing_fixed, plotsize_fixed] * (len(rows) - 1),
                      aspect=False)
    for r, _ in enumerate(rows):
        for c, _ in enumerate(titles):
            main_ax[len(rows) - r - 1, c].set_axes_locator(divider.new_locator(nx=2*c, ny=2*r))
    axs = main_ax if len(rows) > 1 else main_ax[np.newaxis, :]

    fig.supxlabel(s.xlabel,
                  x=(s.left_margin + inner_width/2)/width,
                  y=(s.bottom_margin - s.xlabel_padding)/height,
                  fontsize=s.biglabel)
    fig.supylabel(s.ylabel,
                  x=(s.left_margin - s.ylabel_padding)/width,
                  y=(s.bottom_margin + inner_height/2)/height,
                  fontsize=s.biglabel)

    for ax in fig.get_axes():
        ax.set(xticks=xticks,
               yticks=yticks,
               xticklabels=[],
               yticklabels=[])
        ax.tick_params(axis="both",
                       labelsize=s.ticklabel,
                       size=s.ticksize)
        for spine in ax.spines.values():
            spine.set_linewidth(s.linewidth)
    for i, ax in enumerate(fig.get_axes()):
        ax.text(0,
                1.0 + s.letterposition,
                chr(ord("a") + i),
                transform=ax.transAxes,
                fontsize=s.letterlabel,
                weight="bold")
    for ax in axs[:, 0]:
        ax.set_yticklabels(yticklabels)
    for ax in axs[-1, :]:
        ax.set_xticklabels(xticklabels)
    for c, title in enumerate(titles):
        axs[0, c].set_title(title,
                            pad=s.plotsize * 10,
                            fontsize=s.letterlabel)
    fig.text((s.left_margin + inner_width)/width,
             (s.bottom_margin - s.xlabel_padding)/height,
             "t\n0",
             fontsize=s.biglabel,
             color="grey",
             ha="right")

    # Assign axs objects to variables
    # (AxesImage)

    artists = np.empty_like(axs) 
    dummy_Z = np.zeros((nr, nc))

    for r, _ in enumerate(rows):
        for c, _ in enumerate(titles):
            artists[r, c] = axs[r, c].imshow(dummy_Z,
                                             cmap=s.color_map,
                                             vmin=-1,
                                             vmax=1)

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
