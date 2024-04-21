""" Module to process the plot """

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from modules.update import update_artists


def process_plt(fig, frames, update_data, name):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    if update_data["movie"]:
        movie = {
            "fig": fig,
            "frames": frames,
            "func": update_artists,
            "fargs": (update_data,),
            "blit": True,
        }
        ani = FuncAnimation(**movie)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        update_artists(frames[-1], update_data)
        plt.savefig(f"{name}.png", transparent=False)


def close_plt(fig):
    """Close the figure"""

    plt.close(fig)
