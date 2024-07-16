""" Module to create an animation """

from matplotlib.animation import FuncAnimation


def save_movie(fig, data, options):
    """Function to create a movie"""

    params = {
        "fig": fig,
        "frames": data["frames"],
        "func": data["function"],
        "fargs": (data, options),
        "blit": True,
    }
    ani = FuncAnimation(**params)
    ani.save(f"{data['file_name']}.mp4", writer="ffmpeg", fps=10)
