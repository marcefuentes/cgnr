#!/usr/bin/env python

""" Plot results """

import os
import time
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import Divider, Size

import modules.settings as ss
import modules.modes as mm
from modules.argparse_utils import parse_arguments
from modules.get_df import get_df
from modules.update_zmatrix import update_zmatrix

def update(t, mode, df_mechanisms, movie, text, artists):
    traits = mm.get_traits(mode)
    for r, mechanism in enumerate(df_mechanisms):
        kws = ["cooperation", "correlations", "test"]
        if any(kw in mode for kw in kws) and mechanism == "social":
            continue
        for c, trait in enumerate(traits):
            zmatrix = update_zmatrix(t, df_mechanisms, mechanism, trait, mode)
            artists[r, c].set_array(zmatrix)
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
    xticklabels = [
        f"{xmin:.0f}",
        f"{(xmin + xmax)/2.:.0f}",
        f"{xmax:.0f}"
    ]
    yticklabels = [
        f"{ymax:.1f}",
        f"{(ymin + ymax)/2.:.1f}",
        f"{ymin:.1f}"
    ]

    # Create figure

    traits = mm.get_traits(mode)
    ncols = len(traits)
    nrows = len(mechanisms)
    inner_width = ss.PLOT_SIZE*ncols + ss.SPACING*(ncols - 1)
    inner_height = ss.PLOT_SIZE*nrows + ss.SPACING*(nrows - 1)
    width = inner_width + ss.LEFT_MARGIN + ss.RIGHT_MARGIN
    height = inner_height + ss.TOP_MARGIN + ss.BOTTOM_MARGIN

    fig, main_ax = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(width, height)
    )

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

    plot_size_fixed = Size.Fixed(ss.PLOT_SIZE)
    spacing_fixed = Size.Fixed(ss.SPACING)
    divider = Divider(
        fig,
        (ss.LEFT_MARGIN/width,
        ss.BOTTOM_MARGIN/height,
        inner_width/width,
        inner_height/height),
        [plot_size_fixed] + [spacing_fixed, plot_size_fixed] * (ncols - 1),
        [plot_size_fixed] + [spacing_fixed, plot_size_fixed] * (nrows - 1),
        aspect=False
    )
    for r, _ in enumerate(mechanisms):
        for c, _ in enumerate(traits):
            main_ax[nrows - r - 1, c].set_axes_locator(divider.new_locator(nx=2*c, ny=2*r))

    axs = main_ax if nrows > 1 else main_ax[np.newaxis, :]

    letter_position = 1.0 + ss.LETTER_POSITION
    for i, ax in enumerate(fig.get_axes()):
        letter = chr(ord("a") + i % 26)
        if i >= 26:
            letter = letter + letter
        ax.text(
            0,
            letter_position,
            letter,
            transform=ax.transAxes,
            fontsize=ss.LETTER_LABEL_SIZE,
            weight="bold"
        )
        for spine in ax.spines.values():
            spine.set_linewidth(ss.LINE_WIDTH)
        ax.set(
            xticks=xticks,
            yticks=yticks,
            xticklabels=[],
            yticklabels=[]
        )
        ax.tick_params(
            axis="both",
            labelsize=ss.TICK_LABEL_SIZE,
            size=ss.TICK_SIZE,
        )
    for ax in axs[:, 0]:
        ax.set_yticklabels(yticklabels)
    for ax in axs[-1, :]:
        ax.set_xticklabels(xticklabels)
    for ax, trait in zip(axs[0, :], traits):
        ax.set_title(
            mm.get_title(trait),
            pad=ss.PLOT_SIZE * ss.TITLE_PADDING,
            fontsize=ss.LETTER_LABEL_SIZE
        )

    # Assign axs objects to variables
    # (AxesImage)

    artists = np.empty_like(axs)
    dummy_zmatrix = np.zeros((nr, nc))

    for r, _ in enumerate(mechanisms):
        for c, _ in enumerate(traits):
            artists[r, c] = axs[r, c].imshow(
                dummy_zmatrix,
                cmap=ss.COLOR_MAP,
                vmin=-1,
                vmax=1
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
