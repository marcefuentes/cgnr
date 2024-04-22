""" Module to process the plot """

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def get_update_artists_module(calling_script):
    """Get the update_artists module"""

    if "results" in calling_script:
        from modules_results.update import update_artists
    elif "icurves" in calling_script:
        from modules_theory.update import update_artists
    else:
        raise ValueError("Calling script not recognized")

    return update_artists


def process_plt(fig, frames, update_data, name):
    """Process the figure"""

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    update_artists = get_update_artists_module(name)

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
