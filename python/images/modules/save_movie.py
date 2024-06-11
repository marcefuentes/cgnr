""" Module to create an animation """

from matplotlib.animation import FuncAnimation


def save_movie(fig, update_args, options, data):
    """Function to create a movie"""

    params = {
        "fig": fig,
        "frames": data["frames"],
        "func": update_args["function"],
        "fargs": (
            update_args,
            options,
            data,
        ),
        "blit": True,
    }
    ani = FuncAnimation(**params)
    ani.save(f"{update_args['file_name']}.mp4", writer="ffmpeg", fps=10)
