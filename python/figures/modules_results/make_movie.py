""" Module to process the plot """

from matplotlib.animation import FuncAnimation
from modules_theory.update import update_artists


def make_movie(fig, frames, update_data, name):
    """Function to create a movie from the frames"""

    movie = {
        "fig": fig,
        "frames": frames,
        "func": update_artists,
        "fargs": (update_data,),
        "blit": True,
    }
    ani = FuncAnimation(**movie)
    ani.save(f"{name}.mp4", writer="ffmpeg", fps=10)
