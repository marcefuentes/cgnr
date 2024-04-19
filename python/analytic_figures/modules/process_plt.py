""" Module to process the plot """

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from modules.modes import all_traits
from modules.update import update


def process_plt(fig, ts, dict_update, name):
    """Process the plot"""

    if dict_update["movie"]:
        dict_movie = {
            "fig": fig,
            "frames": ts,
            "func": update,
            "fargs": (dict_update,),
            "blit": True,
        }
        ani = FuncAnimation(**dict_movie)
        ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
    else:
        if dict_update["mode"] == "all_traits":
            for trait in all_traits:
                dict_update["mode"] = trait
                update(ts[-1], dict_update)
                plt.savefig(f"{name}_{trait}.png", transparent=False)
        else:
            update(ts[-1], dict_update)
            name += f"_{dict_update['mode']}"
            plt.savefig(f"{name}.png", transparent=False)

    plt.close()
