""" Module to process the plot """

from matplotlib.animation import FuncAnimation


def save_movie(fig, frames, kwargs, name):
    """Function to create a movie from the frames"""

    movie = {
        "fig": fig,
        "frames": frames,
        "func": kwargs["update_function"],
        "fargs": (kwargs,),
        "blit": True,
    }
    ani = FuncAnimation(**movie)
    ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
