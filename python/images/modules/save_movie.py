""" Module to process the plot """

from matplotlib.animation import FuncAnimation


def save_movie(fig, frames, update_args, name):
    """Function to create a movie from the frames"""

    movie = {
        "fig": fig,
        "frames": frames,
        "func": update_args["update_function"],
        "fargs": (update_args,),
        "blit": True,
    }
    ani = FuncAnimation(**movie)
    ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
