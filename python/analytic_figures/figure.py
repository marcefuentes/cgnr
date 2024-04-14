#!/usr/bin/env python

""" Creates plots. """

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
from modules.argparse_utils import parse_args
from modules.update_zmatrix import update_zmatrix

def update(t, dict_update):
    """ Update the plot with the data at time t. """

    mode =          dict_update["mode"]
    mode_is_trait = dict_update["mode_is_trait"]
    columns =       dict_update["columns"]
    rows =          dict_update["rows"]
    dfs =           dict_update["dfs"]
    df_none =       dict_update["df_none"]
    df_social =     dict_update["df_social"]
    dffrqs =        dict_update["dffrqs"]
    movie =         dict_update["movie"]
    text =          dict_update["text"]
    artists =       dict_update["artists"]

    dict_z = {}
    dict_z["t"] = t

    if mode_is_trait:
        dict_z["trait"] = mode
    else:
        dict_z["df_none"] = df_none
        dict_z["df_social"] = df_social

    for r, row in enumerate(rows):
        if not mode_is_trait:
            dict_z["df"] = dfs[r]
        for c, column in enumerate(columns):
            if mode_is_trait:
                dict_z["df"] = dfs[r][c]
                dict_z["df_none"] = df_none[r][c]
                dict_z["df_social"] = df_social[r][c]
            else:
                dict_z["trait"] = column
            if row == "none" and mode != "none":
                dict_z["none"] = True
            zmatrix = update_zmatrix(dict_z)
            if dffrqs:
                if mode_is_trait:
                    column = mm.look_in(mm.dict_traits, mode, "frq")
                else:
                    column = mm.look_in(mm.dict_traits, column, "frq")
                for a, alpha in enumerate(dict_update["alphas"]):
                    for e, loges in enumerate(dict_update["logess"]):
                        d = dffrqs[r][
                            (dffrqs[r]["Time"] == t) \
                            & (dffrqs[r]["alpha"] == alpha) \
                            & (dffrqs[r]["logES"] == loges)
                        ]
                        freq_a = [col for col in d.columns if re.match(fr"^{column}\d+$", col)]
                        y = d.loc[:, freq_a].values[0].flatten()
                        artists[r, c, a, e].set_ydata(y)
                        bgcolor = colormaps[ss.COLOR_MAP]((zmatrix[a, e] + 1) / 2)
                        artists[r, c, a, e].axes.set_facecolor(bgcolor)
            else:
                artists[r, c].set_array(zmatrix)
    if movie:
        text.set_text(t)
    return artists.flatten()

def init_artists(axs, nrows, ncols, nr, nc):
    """ Initialize AxesImage artists. """

    artists = np.empty_like(axs)
    dummy_zmatrix = np.zeros((nr, nc))

    for r in range(nrows):
        for c in range(ncols):
            artists[r, c] = axs[r, c].imshow(
                dummy_zmatrix,
                cmap=ss.COLOR_MAP,
                vmin=-1,
                vmax=1
            )
    return artists

def init_artists_histogram(axs, nrows, ncols, nr, nc):
    """ Initialize Line2D artists. """

    artists = np.empty_like(axs)
    x = np.arange(ss.BINS)
    dummy_y = np.zeros_like(x)

    for r in range(nrows):
        for c in range(ncols):
            for a in range(nr):
                for e in range(nc):
                    ax = axs[r, c, a, e]
                    artists[r, c, a, e], = ax.plot(
                        x,
                        dummy_y,
                        c="black",
                        lw=ss.LINE_WIDTH * 2
                    )
    return artists

def prettify_axes(axs, divider, alphas, logess, nrows, ncols, columns, mode_is_trait):
    """ Prettify axes. """

    nr = len(alphas)
    nc = len(logess)

    xticks = [0, 0.5*(nc - 1), nc - 1]
    yticks = [0, 0.5*(nr - 1), nr - 1]
    xmin = min(logess)
    xmax = max(logess)
    ymin = min(alphas)
    ymax = max(alphas)
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

    for r in range(nrows):
        for c in range(ncols):
            axs[nrows - r - 1, c].set_axes_locator(
                divider.new_locator(nx=2*c, ny=2*r)
            )

    i = 0
    letter_position = 1.0 + ss.LETTER_POSITION
    for r in range(nrows):
        for c in range(ncols):
            ax = axs[r, c]
            i = r*ncols + c
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
    for ax, column in zip(axs[0, :], columns):
        if not mode_is_trait:
            ax.set_title(
                mm.look_in(mm.dict_traits, column, "title"),
                pad=ss.PLOT_SIZE * ss.TITLE_PADDING,
                fontsize=ss.LETTER_LABEL_SIZE
            )

    return axs

def prettify_axes_histogram(
    axs,
    divider,
    alphas,
    logess,
    nrows,
    ncols,
    columns,
    mode_is_trait
):
    """ Prettify axes for histogram. """

    nr = len(alphas)
    nc = len(logess)

    xlim = [-2, ss.BINS + 1]
    ylim = [0, 0.25]
    step = int(nr/2)
    letter_position = 1.0 + ss.LETTER_POSITION * nr

    for r in range(nrows):
        for c in range(ncols):
            for a in range(nr):
                inner_y = (nrows - r - 1) * (nr + 1) + nr - a - int(a / nr) - 1
                for e in range(nc):
                    inner_x = c * (nc + 1) + e + int(e / nc)
                    new_locator = divider.new_locator(nx=inner_x, ny=inner_y)
                    ax = axs[r, c, a, e]
                    ax.set_axes_locator(new_locator)
                    for spine in ax.spines.values():
                        spine.set_linewidth(ss.LINE_WIDTH)
                    ax.set(
                        xticks=[],
                        yticks=[],
                        xlim=xlim,
                        ylim=ylim
                    )
                    ax.tick_params(
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
    for c, column in enumerate(columns):
        if not mode_is_trait:
            axs[0, c, 0, int(nc/2)].set_title(
                mm.look_in(mm.dict_traits, column, "title"),
                pad=ss.PLOT_SIZE * ss.TITLE_PADDING,
                fontsize=ss.LETTER_LABEL_SIZE
            )
        for e in range(0, nc, step):
            axs[-1, c, -1, e].set_xticklabels([f"{logess[e]:.0f}"])

    return axs

def fix_positions_histogram(nrows, ncols, nr, nc):
    """ Fix positions for histogram. """

    spacing_fixed = Size.Fixed(ss.SPACING)
    plot_size_fixed = Size.Fixed(ss.PLOT_SIZE/nc)
    column_fixed = (
        [plot_size_fixed] * nc
        + ([spacing_fixed] + [plot_size_fixed] * nc) * (ncols - 1)
    )
    row_fixed = (
        [plot_size_fixed] * nr + ([spacing_fixed]
        + [plot_size_fixed] * nr) * (nrows - 1)
    )
    return column_fixed, row_fixed

def fix_positions(nrows, ncols):
    """ Fix positions. """

    spacing_fixed = Size.Fixed(ss.SPACING)
    plot_size_fixed = Size.Fixed(ss.PLOT_SIZE)
    column_fixed = (
        [plot_size_fixed]
        + [spacing_fixed, plot_size_fixed] * (ncols - 1)
    )
    row_fixed = (
        [plot_size_fixed]
        + [spacing_fixed, plot_size_fixed] * (nrows - 1)
    )
    return column_fixed, row_fixed

def prettify_fig(fig, measurements, column_fixed, row_fixed):
    """ Prettify the figure. """

    width = measurements["width"]
    height = measurements["height"]
    inner_width = measurements["inner_width"]
    inner_height = measurements["inner_height"]

    divider = Divider(
        fig,
        (ss.LEFT_MARGIN/width,
        ss.BOTTOM_MARGIN/height,
        inner_width/width,
        inner_height/height),
        column_fixed,
        row_fixed,
        aspect=False
    )

    fig.supxlabel(
        t=ss.X_LABEL,
        x=(ss.LEFT_MARGIN + inner_width/2)/width,
        y=(ss.BOTTOM_MARGIN - ss.X_LABEL_SIZE)/height,
        fontsize=ss.BIG_LABEL_SIZE
    )
    fig.supylabel(
        t=ss.Y_LABEL,
        x=(ss.LEFT_MARGIN - ss.Y_LABEL_SIZE)/width,
        y=(ss.BOTTOM_MARGIN + inner_height/2)/height,
        fontsize=ss.BIG_LABEL_SIZE
    )

    if ss.PRINT_FOLDER:
        bottom_text = os.path.basename(os.getcwd())
    else:
        bottom_text = ""
    fig.text(
        x=(ss.LEFT_MARGIN + inner_width)/width,
        y=(ss.BOTTOM_MARGIN - ss.X_LABEL_SIZE)/height,
        s=bottom_text,
        fontsize=ss.TICK_LABEL_SIZE,
        color="grey",
        ha="right"
    )

    return divider

def add_colorbar(fig, measurements, nc):
    """ Add colorbar. """

    width = measurements["width"]
    height = measurements["height"]
    inner_width = measurements["inner_width"]
    inner_height = measurements["inner_height"]

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

def create_fig(nrows, ncols, measurements, alphas, logess, columns, mode_is_trait):
    """ Create the figure. """

    width = measurements["width"]
    height = measurements["height"]

    fig, main_ax = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(width, height)
    )
    column_fixed, row_fixed = fix_positions(nrows, ncols)
    axs = main_ax if nrows > 1 else main_ax[np.newaxis, :]
    divider = prettify_fig(
        fig,
        measurements,
        column_fixed,
        row_fixed
    )
    axs = prettify_axes(
        axs,
        divider,
        alphas,
        logess,
        nrows,
        ncols,
        columns,
        mode_is_trait
    )
    artists = init_artists(axs, nrows, ncols, len(alphas), len(logess))
    add_colorbar(fig, measurements, len(logess))

    return fig, artists

def create_fig_histogram(nrows, ncols, measurements, alphas, logess, columns, mode_is_trait):
    """ Create the figure with histogram. """

    width = measurements["width"]
    height = measurements["height"]
    nc = len(logess)
    nr = len(alphas)

    fig = plt.figure(figsize=(width, height))
    column_fixed, row_fixed = fix_positions_histogram(nrows, ncols, nr, nc)
    outergrid = fig.add_gridspec(nrows=nrows, ncols=ncols)
    axs = np.empty((nrows, ncols, nr, nc), dtype=object)
    for r in range(nrows):
        for c in range(ncols):
            grid = outergrid[r, c].subgridspec(
                nrows=nr,
                ncols=nc,
                hspace=0.0,
                wspace=0.0
            )
            axs[r, c] = grid.subplots()
    divider = prettify_fig(
        fig,
        measurements,
        column_fixed,
        row_fixed
    )
    axs = prettify_axes_histogram(
        axs,
        divider,
        alphas,
        logess,
        nrows,
        ncols,
        columns,
        mode_is_trait
    )
    artists = init_artists_histogram(axs, nrows, ncols, nr, nc)
    add_colorbar(fig, measurements, nc)

    return fig, artists

def main(mode, histogram=False, movie=False, mode_is_trait=False):
    """ Create the figure. """

    start_time = time.perf_counter()
    this_script = os.path.basename(__file__)
    script_name = this_script.split(".")[0]

    # Set figure properties

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    # Get data

    if mode_is_trait:
        dfs, df_none, df_social, dffrqs = mm.get_data_trait(histogram, movie)
        df = dfs[0][0]
    else:
        dfs, df_none, df_social, dffrqs = mm.get_data_variant(mode, histogram, movie)
        df = df_none

    ts = df.Time.unique()
    alphas = np.sort(df["alpha"].unique())[::-1]
    logess = np.sort(df["logES"].unique())

    rows = mm.get_rows(mode)
    columns = mm.get_columns(mode)
    nrows = len(rows)
    ncols = len(columns)

    inner_width = ss.PLOT_SIZE*ncols + ss.SPACING*(ncols - 1)
    inner_height = ss.PLOT_SIZE*nrows + ss.SPACING*(nrows - 1)
    width = inner_width + ss.LEFT_MARGIN + ss.RIGHT_MARGIN
    height = inner_height + ss.TOP_MARGIN + ss.BOTTOM_MARGIN
    measurements = {
        "width": width,
        "height": height,
        "inner_width": inner_width,
        "inner_height": inner_height
    }

    if histogram:
        fig, artists = create_fig_histogram(
            nrows,
            ncols,
            measurements,
            alphas,
            logess,
            columns,
            mode_is_trait
        )
    else:
        fig, artists = create_fig(
            nrows,
            ncols,
            measurements,
            alphas,
            logess,
            columns,
            mode_is_trait
            )

    # Add data and save

    name = f"{script_name}_{mode}"
    if histogram:
        name = f"{name}_histogram"

    dict_update = {
        "mode": mode,
        "mode_is_trait": mode_is_trait,
        "columns": columns,
        "rows": rows,
        "dfs": dfs,
        "df_none": df_none,
        "df_social": df_social,
        "dffrqs": dffrqs,
        "movie": movie,
        "text": fig.texts[2],
        "artists": artists
    }
    if histogram:
        dict_update["alphas"] = alphas
        dict_update["logess"] = logess

    if movie:
        dict_animation = {
            "fig": fig,
            "frames": ts,
            "func": update,
            "fargs": (dict_update,),
            "blit": True
        }
        ani = FuncAnimation(**dict_animation)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        update(ts[-1], dict_update)
        plt.savefig(f"{name}.png", transparent=False)
    plt.close()

    end_time = time.perf_counter()
    print(f"\nTime elapsed: {(end_time - start_time):.2f} seconds")

if __name__ == "__main__":
    args, is_trait = parse_args()
    main(
        mode=args.mode,
        histogram=args.histogram,
        movie=args.movie,
        mode_is_trait=is_trait
    )
