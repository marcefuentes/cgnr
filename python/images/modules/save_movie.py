""" Module to create an animation """

from matplotlib.animation import FuncAnimation


def save_movie(fig, data):
    """Function to create a movie"""

    params = {
        "fig": fig,
        "frames": data["frames"],
        "func": data["function"],
        "fargs": (data,),
        "blit": True,
    }
    ani = FuncAnimation(**params)
    ani.save(f"{data['file_name']}.mp4", writer="ffmpeg", fps=10)
