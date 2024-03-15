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

from main_figures import settings as ss
from main_figures import modes as mm
from main_figures.get_df import get_df
from main_figures.update_Z import update_Z

def update(t, mode, df_mechanisms, movie, text, artists): 
    traits = mm.get_traits(mode)
    for r, mechanism in enumerate(df_mechanisms):
        if ("cooperation" in mode or "correlations" in mode or "test" in mode) and mechanism == "social":
            continue
        for c, trait in enumerate(traits):
            Z = update_Z(t, df_mechanisms, mechanism, trait, mode)
            artists[r, c].set_array(Z) 
    if movie:
        text.set_text(t)
    elif ss.print_folder:
        text.set_text(os.path.basename(os.getcwd()))
    else:
        text.set_text("")
    return artists.flatten()

def main(mode, movie):

    this_script = os.path.basename(__file__)
    script_name = this_script.split(".")[0]

    # Set figure properties

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    # Get data

    mechanisms = mm.get_mechanisms(mode)
    df_mechanisms = {}

    for mechanism in mechanisms:
        df_mechanisms[mechanism] = get_df(mechanism, "csv", movie)
    if "social" not in mechanisms:
        df_mechanisms["social"] = get_df("social", "csv", movie)
    df = df_mechanisms[mechanisms[0]]
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

    traits = mm.get_traits(mode)
    ncols = len(traits)
    nrows = len(mechanisms)
    inner_width = ss.plotsize*ncols + ss.spacing*(ncols - 1)
    inner_height = ss.plotsize*nrows + ss.spacing*(nrows - 1)
    width = inner_width + ss.left_margin + ss.right_margin
    height = inner_height + ss.top_margin + ss.bottom_margin

    fig, main_ax = plt.subplots(nrows=nrows,
                                ncols=ncols,
                                figsize=(width, height))

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

    plotsize_fixed = Size.Fixed(ss.plotsize)
    spacing_fixed = Size.Fixed(ss.spacing)
    divider = Divider(fig,
                      (ss.left_margin/width,
                       ss.bottom_margin/height,
                       inner_width/width,
                       inner_height/height),
                      [plotsize_fixed] + [spacing_fixed, plotsize_fixed] * (ncols - 1),
                      [plotsize_fixed] + [spacing_fixed, plotsize_fixed] * (nrows - 1),
                      aspect=False)
    for r, _ in enumerate(mechanisms):
        for c, _ in enumerate(traits):
            main_ax[nrows - r - 1, c].set_axes_locator(divider.new_locator(nx=2*c, ny=2*r))

    axs = main_ax if nrows > 1 else main_ax[np.newaxis, :]

    letterposition = 1.0 + ss.letterposition
    for i, ax in enumerate(fig.get_axes()):
        ax.text(0,
                letterposition,
                chr(ord("a") + i),
                transform=ax.transAxes,
                fontsize=ss.letterlabel,
                weight="bold")
        for spine in ax.spines.values():
            spine.set_linewidth(ss.linewidth)
        ax.set(xticks=xticks,
               yticks=yticks,
               xticklabels=[],
               yticklabels=[])
        ax.tick_params(axis="both",
                       labelsize=ss.ticklabel,
                       size=ss.ticksize)
    for ax in axs[:, 0]:
        ax.set_yticklabels(yticklabels)
    for ax in axs[-1, :]:
        ax.set_xticklabels(xticklabels)
    for ax, trait in zip(axs[0, :], traits):
        ax.set_title(mm.get_title(trait),
                     pad=ss.plotsize * ss.titlepad,
                     fontsize=ss.letterlabel)

    # Assign axs objects to variables
    # (AxesImage)

    artists = np.empty_like(axs) 
    dummy_Z = np.zeros((nr, nc))

    for r, _ in enumerate(mechanisms):
        for c, _ in enumerate(traits):
            artists[r, c] = axs[r, c].imshow(dummy_Z,
                                             cmap=ss.color_map,
                                             vmin=-1,
                                             vmax=1)

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
                                   movie,
                                   fig.texts[2],
                                   artists,),
                            blit=True)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        update(ts[-1],
               mode,
               df_mechanisms,
               movie,
               fig.texts[2],
               artists,)
        plt.savefig(f"{name}.png", transparent=False)
    plt.close()

if __name__ == "__main__":

    start_time = time.perf_counter()

    parser = argparse.ArgumentParser(description="Results plots",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("mode", help="Mode: demography or cooperation")
    parser.add_argument("movie", nargs="?", default=False, help="Enable movie")
    args = parser.parse_args()

    main(args.mode, args.movie)

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")
