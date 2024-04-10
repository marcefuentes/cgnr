#!/usr/bin/env python

""" Creates a plot with the frequency of each trait for each mechanism. """

import os
import re
import time
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import ScalarMappable
from matplotlib import colormaps
from mpl_toolkits.axes_grid1 import Divider, Size

import modules.settings as ss
import modules.modes as mm
from modules.argparse_utils import parse_arguments
from modules.get_df import get_df
from modules.update_zmatrix import update_zmatrix

def update(t, mode, df_mechanisms, dffrq_mechanisms, movie, text, artists):
    alphas = np.sort(df_mechanisms["none"]["alpha"].unique())[::-1]
    logess = np.sort(df_mechanisms["none"]["logES"].unique())
    traits = mm.get_traits(mode)
    for r, mechanism in enumerate(df_mechanisms):
        kws = ["cooperation", "correlations", "test"]
        if any(kw in mode for kw in kws) and mechanism == "social":
            continue
        for c, trait in enumerate(traits):
            zmatrix = update_zmatrix(t, df_mechanisms, mechanism, trait, mode)
            for a, alpha in enumerate(alphas):
                for e, loges in enumerate(logess):
                    d = dffrq_mechanisms[mechanism][
                        (dffrq_mechanisms[mechanism]["Time"] == t) \
                        & (dffrq_mechanisms[mechanism]["alpha"] == alpha) \
                        & (dffrq_mechanisms[mechanism]["logES"] == loges)
                    ]
                    freq_a = [col for col in d.columns if re.match(fr"^{trait}\d+$", col)]
                    y = d.loc[:, freq_a].values[0].flatten()
                    artists[r, c, a, e].set_ydata(y)
                    bgcolor = colormaps[ss.COLOR_MAP]((zmatrix[a, e] + 1) / 2)
                    artists[r, c, a, e].axes.set_facecolor(bgcolor)
    if movie:
        text.set_text(t)
    elif ss.PRINT_FOLDER:
        text.set_text(os.path.basename(os.getcwd()))
    else:
        text.set_text("")
    return artists.flatten()

def main(mode, movie=False):

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
    xlim = [-2, ss.BINS + 1]
    ylim = [0, 0.25]
    step = int(nr/2)
    alphas = np.sort(df["alpha"].unique())[::-1]
    logess = np.sort(df["logES"].unique())
    letter_position = 1.0 + ss.LETTER_POSITION * nr

    # Create figure

    traits = mm.get_traits(mode)
    ncols = len(traits)
    nrows = len(mechanisms)
    inner_width = ss.PLOT_SIZE*ncols + ss.SPACING*(ncols - 1)
    inner_height = ss.PLOT_SIZE*nrows + ss.SPACING*(nrows - 1)
    width = inner_width + ss.LEFT_MARGIN + ss.RIGHT_MARGIN
    height = inner_height + ss.TOP_MARGIN + ss.BOTTOM_MARGIN

    fig = plt.figure(figsize=(width, height))
    fig.supxlabel(
        ss.X_LABEL,
        x=(ss.LEFT_MARGIN + inner_width/2)/width,
        y=(ss.BOTTOM_MARGIN - ss.X_LABEL_SIZE)/height,
        fontsize=ss.BIG_LABEL_SIZE
    )
    fig.supylabel(
        ss.Y_LABEL,
        x=(ss.LEFT_MARGIN - ss.Y_LABEL_SIZE)/width,
        y=(ss.BOTTOM_MARGIN + inner_height/2)/height,
        fontsize=ss.BIG_LABEL_SIZE
    )
    fig.text(
        (ss.LEFT_MARGIN + inner_width)/width,
        (ss.BOTTOM_MARGIN - ss.X_LABEL_SIZE)/height,
        "",
        fontsize=ss.TICK_LABEL_SIZE,
        color="grey",
        ha="right"
    )

    plot_size_fixed = Size.Fixed(ss.PLOT_SIZE/nc)
    spacing_fixed = Size.Fixed(ss.SPACING)
    divider = Divider(
        fig,
        (ss.LEFT_MARGIN/width,
        ss.BOTTOM_MARGIN/height,
        inner_width/width,
        inner_height/height),
        [plot_size_fixed] * nc + ([spacing_fixed] + [plot_size_fixed] * nc) * (ncols - 1),
        [plot_size_fixed] * nr + ([spacing_fixed] + [plot_size_fixed] * nr) * (nrows - 1),
        aspect=False
    )

    outergrid = fig.add_gridspec(nrows=nrows, ncols=ncols)
    axs = np.empty((nrows, ncols, nr, nc), dtype=object)

    for r, _ in enumerate(mechanisms):
        for c, _ in enumerate(traits):
            grid = outergrid[r, c].subgridspec(
                nrows=nr,
                ncols=nc,
                hspace=0.0,
                wspace=0.0
            )
            axs[r, c] = grid.subplots()
            for a in range(nr):
                inner_y = (nrows - r - 1) * (nr + 1) + nr - a - int(a / nr) - 1
                for e in range(nc):
                    inner_x = c * (nc + 1) + e + int(e / nc)
                    axs[r, c, a, e].set_axes_locator(divider.new_locator(nx=inner_x, ny=inner_y))
                    for spine in axs[r, c, a, e].spines.values():
                        spine.set_linewidth(ss.LINE_WIDTH)
                    axs[r, c, a, e].set(
                        xticks=[],
                        yticks=[],
                        xlim=xlim,
                        ylim=ylim
                    )
                    axs[r, c, a, e].tick_params(
                        axis="both",
                        labelsize=ss.TICK_LABEL_SIZE,
                        size=ss.TICK_SIZE
                    )
            i = r*ncols + c
            letter = chr(ord("a") + i % 26)
            if i >= 26:
                letter = letter + letter
            axs[r, c, 0, 0].text(
                0,
                letter_position,
                letter,
                fontsize=ss.LETTER_LABEL_SIZE,
                transform=axs[r, c, 0, 0].transAxes,
                weight="bold"
            )
            for a in range(0, nr, step):
                axs[r, c, a, 0].set(yticks=[ylim[1]/2], yticklabels=[])
            for e in range(0, nc, step):
                axs[r, c, -1, e].set(xticks=[xlim[1]/2], xticklabels=[])
        for a in range(0, nr, step):
            axs[r, 0, a, 0].set_yticklabels([alphas[a]])
    for c, trait in enumerate(traits):
        axs[0, c, 0, int(nc/2)].set_title(
            mm.get_title(trait),
            pad=ss.PLOT_SIZE * ss.TITLE_PADDING,
            fontsize=ss.LETTER_LABEL_SIZE
        )
        for e in range(0, nc, step):
            axs[-1, c, -1, e].set_xticklabels([f"{logess[e]:.0f}"])

    # Assign axs objects to variables
    # (Line2D)

    artists = np.empty_like(axs)
    x = np.arange(ss.BINS)
    dummy_y = np.zeros_like(x)

    for r, _ in enumerate(mechanisms):
        for c, _ in enumerate(traits):
            for a, _ in enumerate(alphas):
                for e, _ in enumerate(logess):
                    ax = axs[r, c, a, e]
                    artists[r, c, a, e], = ax.plot(
                        x,
                        dummy_y,
                        c="black",
                        lw=ss.LINE_WIDTH * 2
                    )

    sm = ScalarMappable(cmap=ss.COLOR_MAP, norm=plt.Normalize(-1, 1))
    cax = fig.add_axes([
        (ss.LEFT_MARGIN + inner_width + ss.SPACING)/width,
        (ss.BOTTOM_MARGIN + inner_height/2 - ss.PLOT_SIZE/2)/height,
        (ss.PLOT_SIZE/nc)/width,
        ss.PLOT_SIZE/height
    ]) # [left, bottom, width, height]
    cbar = fig.colorbar(
        sm,
        cax=cax,
        ticks=[-1, 0, 1]
    )
    cbar.ax.tick_params(labelsize=ss.TICK_LABEL_SIZE, size=ss.TICK_SIZE)
    cbar.outline.set_linewidth(ss.LINE_WIDTH)

    # Save figure

    name = f"{script_name}_{mode}"
    if movie:
        ani = FuncAnimation(
            fig,
            update,
            frames=ts,
            fargs=(
                mode,
                df_mechanisms,
                dffrq_mechanisms,
                movie,
                fig.texts[2],
                artists,
            ),
            blit=True
        )
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        update(
            ts[-1],
            mode,
            df_mechanisms,
            dffrq_mechanisms,
            movie,
            fig.texts[2],
            artists,
        )
        plt.savefig(f"{name}.png", transparent=False)
    plt.close()

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")

if __name__ == "__main__":
    trait_choices = list(mm.traits.keys())
    args = parse_arguments(trait_choices)
    main(mode=args.mode, movie=args.movie)
